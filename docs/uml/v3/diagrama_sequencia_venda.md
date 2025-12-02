# Diagrama de Sequência — Fluxo de Venda e Relatório (versão aprimorada)

Este arquivo descreve, em linguagem simples, os fluxos de venda e geração de relatórios no sistema.
Ele evita ferramentas como Mermaid e usa um esquema textual/ASCII fácil de ler para estudantes com conhecimento básico.

### Atores / Componentes
- Usuário: pessoa que usa a interface (clicando botões).
- Interface (Streamlit): páginas de vendas e relatórios.
- `main.py` (navegação): chama a função da página quando o usuário escolhe a aba.
- `pag_venda` / `SaleManager`: lógica de vendas (adicionar ao carrinho, finalizar).
- `Cart`: estrutura que guarda itens temporariamente (em `st.session_state`).
- `pag_produtos` / `ProdutoManager`: lista e atualiza produtos/estoque.
- `pag_clientes`: lista e valida clientes.
- `pag_relatorio` / `RelatorioManager`: gera relatórios de vendas, PDFs de análise e recibos.
- `st.session_state`: armazenamento compartilhado (produtos, cart, sales, next_sale_id).

---

### Visão passo a passo (venda e relatório)

**Fluxo de Venda:**
1. Usuário seleciona a página "Vendas" na interface.
2. O `main.py` chama `pag_venda.render_page()` para mostrar a página.
3. `pag_venda` cria um `SaleManager` que garante que clientes e produtos existam (invoca `pag_clientes` e `pag_produtos`).
4. A página mostra o catálogo de produtos (dados vindos de `st.session_state['produtos']`).
5. Usuário clica "Adicionar" num produto X com quantidade Q.
6. A interface pede a `SaleManager` para adicionar ao carrinho (`add_product_to_cart(nome, Q)`).
7. `SaleManager` consulta os produtos (via `ProdutoManager` ou `st.session_state`) e verifica o estoque.
   - Se houver estoque suficiente: `Cart` é atualizado (salva em `st.session_state['cart']`) e a interface mostra o item no carrinho.
   - Se não houver estoque suficiente: a interface exibe uma mensagem de aviso e não adiciona.
8. Usuário pode visualizar os itens do carrinho e remover itens.
9. Ao remover, o `Cart` exclui o item e atualiza `st.session_state`.
10. Usuário clica "Finalizar Venda".
11. A interface chama `SaleManager.finalize_sale(cliente_id)`.
12. `SaleManager` valida o cliente (consulta `pag_clientes`).
    - Se cliente inválido: exibe erro e cancela.
13. `SaleManager` obtém os itens do `Cart` e, para cada item, tenta decrementar o estoque em `produtos`.
    - Se algum decremento falhar (estoque insuficiente entre o momento da adição e o checkout): a venda é abortada e uma mensagem é exibida.
14. Se tudo estiver OK: `SaleManager` cria um objeto `sale` (com id, cliente, itens, total, data), guarda em `st.session_state['sales']` e limpa o `cart`.
15. `SaleManager` confirma sucesso na interface. Se `pag_relatorio` oferecer `generate_sale_pdf`, um PDF de recibo pode ser gerado e oferecido para download.

**Fluxo de Relatório de Vendas:**
16. Usuário seleciona a página "Relatórios" na interface.
17. O `main.py` chama `pag_relatorio.render_page()` para mostrar a página.
18. `pag_relatorio` cria um `RelatorioManager` que acessa as vendas em `st.session_state['sales']`.
19. A interface exibe filtros de período, métricas agregadas e lista de vendas.
20. Usuário solicita geração de relatório PDF.
21. `RelatorioManager` filtra, agrega e prepara os dados, gera o PDF e disponibiliza para download.

---

### Diagrama ASCII (venda e relatório)

As colunas abaixo representam os participantes. As setas indicam a direção da chamada/ação.

```
Usuário      Interface      pag_venda/SaleMgr      Cart      pag_produtos      pag_clientes      pag_relatorio/RelatorioMgr      st.session_state
--------     ----------     -------------------    -----     -------------     -------------     --------------------------     ----------------
   |             |                  |                |            |                  |                  |                        |
   |--(1) escolha página Vendas -->|                  |            |                  |                  |                        |
   |             |--(2) chama render_page()--------->|            |                  |                  |                        |
   |             |                  |--(3) cria SaleManager -->|      |                  |                  |                        |
   |             |                  |                |            |                  |                  |                        |
   |--(5) clica Adicionar (X,Q)--> |--(6) add_product->|--(7) add-> |            |--(7.1) lê produtos->|                  |                        |
   |             |                  |                |            |<-(produtos)------|                  |                        |
   |             |<--mensagem/atualiza carrinho-----|                |                  |                  |                        |
   |             |                  |                |            |                  |                  |                        |
   |--(10) clica Finalizar ------->|--(11) finalize_sale(cliente_id) --->|        |                  |                  |                        |
   |             |                  |--(12) valida cliente ---------->|        |                  |                  |                        |
   |             |                  |--(13) decrementa estoque para cada item ->pag_produtos-->|                |                        |
   |             |                  |                                                        |--(14) grava sale em st.session_state -->|                        |
   |             |<--(15) sucesso / download do PDF --(se houver)-- pag_relatorio retorna PDF -->|                        |
   |             |                  |                |            |                  |                  |                        |
   |--(16) escolha página Relatórios -->|             |           |                  |                  |                        |
   |             |--(17) chama render_page()--------------------->|                  |                  |--(18) cria RelatorioManager -->|
   |             |                  |                |            |                  |                  |                        |
   |             |                  |                |            |                  |                  |--(19) acessa vendas em st.session_state -->|
   |             |                  |                |            |                  |                  |--(20) filtra/agrega dados, exibe métricas |
   |             |                  |                |            |                  |                  |--(21) gera PDF e retorna para download |
```

Obs: O fluxo de relatório pode ser acionado independentemente do fluxo de vendas, e utiliza os dados de vendas registrados.

---

### Ligação direta com o código (onde olhar)
- Fluxo principal de vendas: `src/pag_venda.py` → função `render_page()` e classe `SaleManager`.
- Funções úteis: `add_product_to_cart`, `finalize_sale`, `get_products_list`, `decrement_product_stock`.
- Produtos: `src/pag_produtos.py` → `ProdutoManager` (função `listar_produtos` e manipulação de `st.session_state['produtos']`).
- Clientes: `src/pag_clientes.py` → funções que retornam clientes (verificar `get_customers` ou similar).
- Relatórios: `src/pag_relatorio.py` → classe `RelatorioManager`, função `render_page`, função `generate_sale_pdf` e geração de PDF de análise.
