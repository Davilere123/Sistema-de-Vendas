
# Arquitetura Geral do Sistema — Modelo MVC

Este documento descreve a arquitetura proposta para o "Sistema de Vendas" usando o padrão Model-View-Controller (MVC), mapeando os arquivos atuais do repositório para cada camada e propondo uma estrutura de diretórios e próximas ações de refatoração.

## Resumo

- Objetivo: separar responsabilidades entre Model (dados e persistência), View (interface Streamlit) e Controller (regras de negócio), facilitando testes, manutenção e evolução.
- Situação atual: as páginas `pag_*.py` misturam UI (Streamlit), modelos (dataclasses) e lógica (managers), e usam `st.session_state` como armazenamento volátil.

## Visão Geral do Padrão MVC

- Model: representa entidades de negócio (Produto, Cliente, Venda, etc.) e a persistência (hoje `st.session_state`).
- View: responsabilidade de renderizar a interface (páginas Streamlit) e capturar eventos do usuário.
- Controller: contém a lógica de aplicação (validações, orquestração entre models e views, regras de negócio — ex.: finalizar venda, decrementar estoque).

Fluxo básico: View (usuário) -> Controller (valida/ordena) -> Model (atualiza) -> View (re-render)

## Mapeamento atual (arquivos em `src/`)

- Model (dados / armazenamento)
  - `pag_produtos.py` — define `Produto` (dataclass) e usa `st.session_state["produtos"]`.
  - `pag_venda.py` — define `CartItem` e registra vendas em `st.session_state["sales"]` / `next_sale_id`.
  - `pag_clientes.py` — (presumido) gerencia clientes e armazena em `st.session_state["customers"]`.

- View (UI / Streamlit)
  - `main.py` — roteador/ponto de entrada que monta as páginas com Streamlit.
  - `pag_principal.py` — tela inicial (saudação, boas-vindas).
  - `pag_ajuda.py` — página de ajuda e link para o GitHub.
  - Partes de `pag_produtos.py` e `pag_venda.py` que fazem chamadas a `st.*` compõem a View atualmente.

- Controller (lógica / regras)
  - `pag_produtos.py` — `ProdutoManager` (CRUD, validações) mistura controller e view.
  - `pag_venda.py` — `SaleManager`, `Cart`, `finalize_sale`, `add_product_to_cart`, `decrement_product_stock` (regras de negócio e fluxo).
  - `pag_clientes.py` — (presumido) funções de criação/consulta/remoção de clientes.

Observação: hoje a separação está misturada; a proposta é extrair dataclasses/modelos e lógica para módulos específicos.

## Exemplo de fluxo (Adicionar produto e finalizar venda)

1. Usuário clica em "Adicionar" na View (`pag_venda` / catálogo).
2. View chama `SaleManager.add_product_to_cart(...)` (Controller).
3. Controller valida estoque e atualiza Model (`st.session_state["cart"]` / produtos).
4. Ao finalizar, Controller (`finalize_sale`) decremeta estoque, cria a venda, salva em `st.session_state["sales"]` e retorna recibo.

## Proposta de layout de diretórios (refatoração)

Sugestão de estrutura dentro de `src/`:

- `src/models/`
  - `product.py`     — dataclass `Produto` e métodos auxiliares simples
  - `customer.py`    — dataclass `Cliente`
  - `sale.py`        — `Sale`, `CartItem`
  - `storage.py`     — adaptador de persistência (interface que hoje usa `st.session_state`, permitindo trocar para SQLite/TinyDB)

- `src/controllers/`
  - `product_controller.py` — lógica CRUD e validações (antes `ProdutoManager`)
  - `sale_controller.py`    — `SaleManager`, regras de venda e orquestração
  - `customer_controller.py`— lógica de clientes

- `src/views/` (cada arquivo expõe `render_page(session_state=None)`)
  - `main.py` / `app.py`      — entrypoint e roteamento (substitui o atual `main.py` ou o adapta)
  - `products_view.py`       — UI de cadastro/listagem/remoção de produtos
  - `sales_view.py`          — UI do carrinho/checkout
  - `customers_view.py`      — UI de gerenciamento de clientes
  - `help_view.py`           — página de ajuda
  - `reports_view.py`        — geração/visualização de relatórios (PDF)

- `src/utils/` ou `src/services/`
  - `pdf_generator.py`, `formatting.py` e helpers reutilizáveis

## Vantagens dessa separação

- Testabilidade: controllers e models testáveis sem depender do Streamlit.
- Substituição de persistência: trocar `storage.py` para usar SQLite sem alterar controllers.
- Responsabilidade única: views apenas renderizam, controllers implementam regras, models guardam dados.

## Recomendações práticas e passos imediatos

1. Criar `src/models/` e mover/definir `Produto`, `CartItem`, `Sale` e `Cliente` como dataclasses.
2. Criar `src/models/storage.py` que exponha API: `get_products()`, `save_product()`, `get_customers()`, `save_sale()` — inicialmente implementado sobre `st.session_state`.
3. Extrair a lógica de `ProdutoManager` e `SaleManager` para `src/controllers/` (expor interfaces simples usadas pelas views).
4. Adaptar as páginas `pag_*.py` para se tornarem simples `views/` que chamam controllers e permanecem como pontos de integração com Streamlit (método `render_page(session_state)`).
5. Adicionar testes unitários para controllers (ex.: `tests/test_sale_controller.py`) cobrindo finalização de vendas, decremento de estoque e erros de validação.

## Diagrama ASCII (resumido)

View (Streamlit pages: `views/*.py`)
  |
  v
Controller (`controllers/*.py`) <--> Models (`models/*.py`)
  |
  v
Storage adapter (`models/storage.py` -> `st.session_state` / DB)

## Próximos passos sugeridos

- Opção A — Refatoração mínima (recomendada inicialmente): criar `models/storage.py` e `controllers/*` esqueleto; adaptar `pag_*.py` para usar os controllers. Isto reduz acoplamento sem grandes renomeações.
- Opção B — Refatoração completa: reorganizar em `src/models/`, `src/controllers/`, `src/views/` e mover/renomear arquivos. Requer cuidado com imports e testes.
- Opção C — Persistência: depois da separação, implementar persistência permanente (SQLite/TinyDB) substituindo `storage.py`.

Se desejar, posso aplicar a Opção A automaticamente (criar os módulos adaptadores e atualizar `pag_produtos.py` / `pag_venda.py` para usar a nova camada de storage/controllers). Indique qual opção prefere e eu procedo.
