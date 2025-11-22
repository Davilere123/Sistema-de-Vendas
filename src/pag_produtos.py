import streamlit as st  # importando o streamlit

# Textos explicativos --------------------
st.title("Gerenciamento de produtos 📦")
st.header("Aqui você pode gerenciar seus produtos.")

# Título da página
st.subheader("🛒 Cadastro de Produtos")

# Inicializar o "banco de dados" na sessão
if "produtos" not in st.session_state:
    st.session_state.produtos = []

# Formulário de cadastro
with st.form("form_cadastro"):
    nome = st.text_input("Nome do Produto")
    preco = st.number_input("Preço (R$)", min_value=0.0, format="%.2f")
    quantidade = st.number_input("Quantidade de Produtos", min_value=0, step=1)
    enviar = st.form_submit_button("Cadastrar")

    if enviar:
        if nome:
            novo_produto = {"Nome": nome, "Preço": preco, "Quantidade": quantidade}
            st.session_state.produtos.append(novo_produto)
            st.success(f"✅ Produto '{nome}' cadastrado com sucesso!")
        else:
            st.warning("⚠️ O nome do produto é obrigatório!")

# Mostrar lista de produtos cadastrados
st.subheader("📋 Produtos cadastrados")
if st.session_state.produtos:
    st.table(st.session_state.produtos)  # Streamlit entende listas de dicionários
else:
    st.info("Nenhum produto cadastrado ainda.")

# Opção de remover produtos
st.subheader("🗑️ Remover Produtos")
if st.session_state.produtos:
    nomes = [p["Nome"] for p in st.session_state.produtos]
    produto_remover = st.selectbox("Selecione o produto para remover", nomes)
    if st.button("Remover"):
        st.session_state.produtos = [
            p for p in st.session_state.produtos if p["Nome"] != produto_remover
        ]
        st.success(f"Produto '{produto_remover}' removido!")
else:
    st.write("Nenhum produto disponível para remover.")
