import streamlit as st

#Definição de paginas
main_page = st.Page("pag_principal.py", title="Início", icon="🏠")
client_page = st.Page("pag_clientes.py", title="Gerenciar clientes", icon="👥")
product_page = st.Page("pag_produtos.py", title="Gerenciar produtos", icon="📦")
report_page = st.Page("pag_relatorio.py", title="Relatórios", icon="📊")
sales_page = st.Page("pag_venda.py", title="Vendas", icon="🛒")
help_page = st.Page("pag_ajuda.py", title="Ajuda", icon="🆘")

pg = st.navigation([main_page, client_page, product_page, report_page, sales_page, help_page])

pg.run()