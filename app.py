import streamlit as st
from fpdf import FPDF
import datetime

#--- Configuração da Página ---
st.set_page_config(
    page_title="Sistema de Vendas de Alimentos",
    page_icon="🍔",
    layout="wide"
)

#--- "Banco de Dados" de Produtos (Mock) ---
#Em um aplicativo real, isso viria de um banco de dados
PRODUCTS = {
    "prod_001": {"name": "Hambúrguer", "price": 25.50, "image": "🍔"},
    "prod_002": {"name": "Pizza", "price": 42.00, "image": "🍕"},
    "prod_003": {"name": "Batata Frita", "price": 12.00, "image": "🍟"},
    "prod_004": {"name": "Refrigerante", "price": 6.50, "image": "🥤"},
    "prod_005": {"name": "Salada", "price": 22.00, "image": "🥗"},
}