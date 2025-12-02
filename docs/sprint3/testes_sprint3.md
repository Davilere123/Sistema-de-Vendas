# Testes unitários

## Gerenciamento de clientes
O cadastro de clientes está funcional. Os clientes (nome, e-mail, telefone e endereço) são registrados, visualizados e removidos corretamente, exceto o cliente padrão criado para testes.

## Gerenciamento de produtos
O cadastro de produtos está funcional. Os produtos (nome, preço e quantidade) são registrados, visualizados e removidos corretamente.  

## Módulo de vendas
Os produtos e clientes registrados são corretamente visualizados. A parte de vender funciona e o estoque é atualizado.

## Sistema de relatórios em PDF
Os relatórios são gerados corretamente e a geração e exportação de PDFs funciona também.

# Testes de integração
Todos os sistemas estão integrados corretamente. O de vendas conversa com o de clientes e produtos, o de relatórios conversa com todos os outros!

# Bugs e pontos de melhoria
O sistema funciona, entretanto, alguns pontos precisam de melhorias:
- A interface dos dois sistemas de cadastro estão muito diferentes. Padronizar a interface é importante para a experiência do usuário;
- A interface do módulo de vendas está meio esquisita e precisa de polimento;
- O sistema de gerenciamento de produtos tem um problema onde a tabela que mostra os clientes não é atualizada quando um é removido. Ela só atualiza ao sair e entrar na página.