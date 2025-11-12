# Documentação da Estrutura de Dados do Sistema de Vendas Simples

Este documento detalha a estrutura de dados do Sistema de Vendas Simples.

## Biblioteca Streamlit e separação em páginas
A biblioteca Streamlit, escolhida para ser feita a interface do sistema, permite a separação por páginas, sendo todas as páginas "reunidas" em um arquivo principal "main.py".  
Cada página é, essencialmente, uma parte diferente do sistema.  
Separamos cada parte em uma página diferente:  
- Página de ajuda - pag_ajuda.py - onde o usuário vai obter ajuda e vai encontrar links importantes, se precisar
- Página de gerenciamento de clientes - pag_clientes.py - onde o usuário vai fazer o gerenciamento dos clientes
- Página de gerenciamento de produtos - pag_produtos.py - onde o usuário vai fazer o gerenciamento dos produtos
- Página de relatórios - pag_relatorio.py - onde o usuário poderá gerar relatórios e exportá-los em PDF
- Página de venda - pag_venda.py - onde o usuário poderá realizar vendas
- Página principal - pag_principal.py - onde o usuário será acolhido e instruído sobre o que fazer  
---
Cada página possui um título, uma descrição e as suas funcionalidades.
---
## Estrutura dos códigos
Cada código deve possuir a seguinte estrutura:
- Importação das bibliotecas necessárias, com o streamlit SEMPRE sendo importado para permitir a integração na interface
- Classes e métodos
> Os códigos devem ser comentados

## Estrutura do repositório
O repositório está estruturado em várias pastas:
- docs: documentos necessários para as sprints e apresentações do trabalho ao professor
- src: os códigos-fonte do projeto
- tests: códigos de teste para testar funcionalidades individuais
- o arquivo README.md: o arquivo que contém a descrição do projeto



