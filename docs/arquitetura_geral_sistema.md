
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

Model (dados / armazenamento)
  - `pag_produtos.py` — define `Produto` (dataclass) e usa `st.session_state["produtos"]`.
  - `pag_venda.py` — define `CartItem` e registra vendas em `st.session_state["sales"]` / `next_sale_id`.
  - `pag_clientes.py` — (presumido) gerencia clientes e armazena em `st.session_state["customers"]`.
  - `pag_relatorio.py` — acessa e manipula dados de vendas via `st.session_state["sales"]` para análise e relatórios.

View (UI / Streamlit)
  - `main.py` — roteador/ponto de entrada que monta as páginas com Streamlit.
  - `pag_principal.py` — tela inicial (saudação, boas-vindas).
  - `pag_ajuda.py` — página de ajuda e link para o GitHub.
  - `pag_relatorio.py` — interface de análise de vendas, métricas, filtro por período e geração de relatórios PDF.
  - Partes de `pag_produtos.py` e `pag_venda.py` que fazem chamadas a `st.*` compõem a View atualmente.

Controller (lógica / regras)
  - `pag_produtos.py` — `ProdutoManager` (CRUD, validações) mistura controller e view.
  - `pag_venda.py` — `SaleManager`, `Cart`, `finalize_sale`, `add_product_to_cart`, `decrement_product_stock` (regras de negócio e fluxo).
  - `pag_clientes.py` — (presumido) funções de criação/consulta/remoção de clientes.
  - `pag_relatorio.py` — `RelatorioManager` (filtragem, agregação, geração de PDF, lógica de análise de vendas).

Observação: hoje a separação está misturada; a proposta é extrair dataclasses/modelos e lógica para módulos específicos.


## Exemplos de fluxo

### Adicionar produto e finalizar venda
1. Usuário clica em "Adicionar" na View (`pag_venda` / catálogo).
2. View chama `SaleManager.add_product_to_cart(...)` (Controller).
3. Controller valida estoque e atualiza Model (`st.session_state["cart"]` / produtos).
4. Ao finalizar, Controller (`finalize_sale`) decremeta estoque, cria a venda, salva em `st.session_state["sales"]` e retorna recibo.

### Gerar relatório de vendas
1. Usuário acessa a página de relatório (`pag_relatorio.py`).
2. View exibe filtro de período, métricas e lista de vendas.
3. View chama métodos do `RelatorioManager` para filtrar, agregar e preparar os dados.
4. Usuário solicita geração de relatório PDF; Controller monta o PDF e disponibiliza para download.

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

## Módulo de Relatórios

O módulo de relatórios foi implementado em `src/pag_relatorio.py` e segue a arquitetura MVC proposta:

- **Model/Controller:**
  - A classe `RelatorioManager` gerencia o acesso aos dados de vendas e a geração dos relatórios, operando sobre `st.session_state.sales`.
  - Funções auxiliares permitem obter a lista de vendas e gerar recibos em PDF para vendas individuais.

- **View:**
  - A função `render_page()` exibe a interface Streamlit para análise de vendas, filtrando por período, mostrando métricas agregadas (total vendido, quantidade de itens, período analisado) e listando as vendas.
  - Permite ao usuário gerar um relatório de análise em PDF, com resumo e detalhes das vendas (top 10), disponível para download.

- **Funcionalidades:**
  - Filtro de vendas por período (N dias).
  - Resumo financeiro e de quantidade.
  - Listagem tabular das vendas.
  - Geração de relatório PDF customizado, incluindo período, totais e detalhes das vendas.
  - Geração de recibo PDF individual para cada venda (função `generate_sale_pdf`).

- **Integração:**
  - O módulo pode ser chamado diretamente pelo roteador principal (`main.py`) ou integrado como uma página do sistema.
  - Utiliza o pacote `fpdf` para geração de PDFs e `pandas` para manipulação dos dados.

- **Sugestão de refatoração futura:**
  - Extrair o gerador de PDF para `src/utils/pdf_generator.py` para uso compartilhado.
  - Permitir exportação dos dados em outros formatos (CSV, Excel).

---

**Exemplo de uso:**

```python
from pag_relatorio import render_page
render_page()
```

---

O módulo de relatórios complementa a arquitetura, fornecendo análise e exportação dos dados de vendas, alinhado ao padrão MVC e à proposta de modularização do sistema.

## Diagrama ASCII (resumido)

View (Streamlit pages: `views/*.py`)
  |
  v
Controller (`controllers/*.py`) <--> Models (`models/*.py`)
  |
  v
Storage adapter (`models/storage.py` -> `st.session_state` / DB)
