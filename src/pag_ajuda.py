import streamlit as st

url_github = "https://github.com/Davilere123/Sistema-de-Vendas"

st.title("Obter ajuda 🆘")
st.header("Aqui você pode encontrar ajuda.")
st.write("Caso possua alguma dúvida sobre o funcionamento do sistema, consulte a documentação disponível no GitHub ou entre em contato com o suporte.")
st.write("[Documentação no GitHub](%s)" % url_github)