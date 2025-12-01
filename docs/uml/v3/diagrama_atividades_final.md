# Diagrama de Atividades UML — Sistema de Vendas (Versão Final)

## Fluxo Principal
1. **Início do Sistema**
2. **Exibe Página Principal**
3. **Usuário escolhe ação:**
    - Gerenciar Produtos
    - Gerenciar Clientes
    - Relatórios
    - Vendas
    - Ajuda

---

## Gerenciamento de Produtos
- Exibe página de produtos
    - Usuário clica em Cadastrar
        - Tem os dados obrigatórios presentes?
            - Se sim: produto é cadastrado/adicionado à lista
            - Se não: avisa que pelo menos o nome é obrigatório e dá erro
    - Usuário clica em Remover
        - Tem um produto selecionado?
            - Se sim: produto é removido da lista
            - Se não: nada acontece, pois não há produto
    - Usuário visualiza lista de produtos

---

## Gerenciamento de Clientes
- Exibe página de clientes
    - Usuário clica em Cadastrar Cliente
        - Tem os dados obrigatórios presentes?
            - Se sim: cliente é cadastrado/adicionado
            - Se não: avisa que pelo menos o nome é obrigatório e dá erro
    - Usuário clica em Remover Cliente
        - É o cliente padrão selecionado?
            - Se sim: dá erro e avisa que o cliente padrão não pode ser removido
            - Se não: cliente selecionado é removido
    - Usuário visualiza lista de clientes

---

## Realizar Venda
- Exibe página de vendas
    - Usuário clica em Adicionar
        - A quantidade do produto é maior que 1?
            - Se sim: produto é colocado no carrinho
            - Se não: não é possível adicionar um produto sem estoque
    - Usuário remove produto do carrinho → Produto removido do carrinho
    - Usuário seleciona cliente
    - Usuário clica em finalizar venda
        - Venda é finalizada
        - Estoque atualizado
        - Recibo gerado

---

## Relatórios
- Exibe página de relatórios
    - Usuário visualiza relatórios → Relatório exibido

---

## Ajuda
- Exibe página de ajuda
    - Usuário acessa documentação → Documentação exibida

---

**Legenda:**
- As atividades principais do sistema estão representadas por caixas.
- Decisões do usuário são representadas por losangos.
- O fluxo cobre cadastro, remoção, visualização de produtos/clientes, realização de vendas, geração de recibos e acesso à ajuda.

> Diagrama gerado com base nos arquivos `pag_principal.py`, `pag_produtos.py`, `pag_venda.py`, `pag_clientes.py` e `pag_ajuda.py`.