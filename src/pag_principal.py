#Importação de bibliotecas -------------------

import streamlit as st #importando o streamlit
from datetime import datetime #importando a bilbioteca datetime para o sistema saber a hora

#Funções --------------------

def get_saudacao(): #função para definir a saudação conforme o horário do dia
    hora_atual = datetime.now().hour #pegando a hora atual do sistema
    if 5 <= hora_atual < 12: #se a hora estiver entre 5 e 12 (manhã)
        return "Bom dia"
    elif 12 <= hora_atual < 18: #se a hora estiver entre 12 e 18 (tarde)
        return "Boa tarde"
    else: #se não for as outras, então é noite
        return "Boa noite"

saudacao = get_saudacao() #salva a saudação em uma variável

#A interface --------------------

st.title("Sistema de Vendas 🛒")
st.header(f"{saudacao}, usuário!")
st.write("Bem-vindo ao sistema de vendas! Essa é a versão inicial da interface.")
