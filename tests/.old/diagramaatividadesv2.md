# Diagrama de Atividades UML — Sistema de Vendas (v2)


## Diagrama de Atividades UML — Sistema de Vendas (v2)

Abaixo está uma descrição textual estruturada do diagrama de atividades, baseada nos códigos do sistema:

### Fluxo Principal
1. **Início do Sistema**
2. **Exibe Página Principal**
3. **Usuário escolhe ação:**
    - Gerenciar Produtos
    - Gerenciar Clientes
    - Relatórios
    - Vendas
    - Ajuda

---

### Gerenciar Produtos
- Exibe página de produtos
    - Usuário cadastra produto → Produto adicionado à lista
    - Usuário remove produto → Produto removido da lista
    - Usuário visualiza lista de produtos

### Realizar Venda
- Exibe página de vendas
    - Usuário adiciona produto ao carrinho → Produto adicionado ao carrinho
    - Usuário remove produto do carrinho → Produto removido do carrinho
    - Usuário seleciona cliente
    - Finaliza venda → Estoque atualizado, Recibo gerado

### Gerenciar Clientes
- Exibe página de clientes
    - Usuário cadastra cliente → Cliente adicionado
    - Usuário remove cliente → Cliente removido
    - Usuário visualiza lista de clientes

### Relatórios
- Exibe página de relatórios
    - Usuário visualiza relatórios → Relatório exibido

### Ajuda
- Exibe página de ajuda
    - Usuário acessa documentação → Documentação exibida

---

**Legenda:**
- As atividades principais do sistema estão listadas por tópicos.
- O fluxo cobre cadastro, remoção, visualização de produtos/clientes, realização de vendas, geração de recibos e acesso à ajuda.

> Diagrama gerado com base nos arquivos `pag_principal.py`, `pag_produtos.py`, `pag_venda.py`, e `pag_ajuda.py`.

---

**Legenda:**
- As atividades principais do sistema estão representadas por caixas.
- Decisões do usuário são representadas por losangos.
- O fluxo cobre cadastro, remoção, visualização de produtos/clientes, realização de vendas, geração de recibos e acesso à ajuda.

> Diagrama gerado com base nos arquivos `pag_principal.py`, `pag_produtos.py`, `pag_venda.py`, e `pag_ajuda.py`.
