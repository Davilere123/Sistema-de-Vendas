import streamlit as st

#Definição de paginas
main_page = st.Page("pag_principal.py", title="Início", icon="🏠")
client_page = st.Page("pag_clientes.py", title="Gerenciar clientes", icon="👥")
product_page = st.Page("pag_produtos.py", title="Gerenciar produtos", icon="📦")
report_page = st.Page("pag_relatorios.py", title="Relatórios", icon="📊")

pg = st.navigation([main_page, client_page, product_page, report_page], menu_title="Menu de Navegação", default_page=main_page)

pg.run()