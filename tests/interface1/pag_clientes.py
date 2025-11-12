import streamlit as st #importando o streamlit
import pandas as pd

#Textos explicativos --------------------
st.title("Gerenciamento de Clientes 👥")
st.header("Aqui você pode gerenciar seus clientes.")

# ==============================================================================
# PARTE 1: LÓGICA / "MÓDULO"
#
# Estas são as funções que outros arquivos (como pag_venda.py)
# podem importar e usar. Elas gerenciam os dados no st.session_state.
# ==============================================================================

def initialize_customers():
    """
    Inicializa o 'banco de dados' de clientes no estado da sessão (session_state).
    Isso garante que os dados não se percam entre as navegações.
    """
    if "customers" not in st.session_state:
        # Usamos um dicionário onde a CHAVE é o ID e o VALOR são os dados.
        # Isso torna a busca por ID (get_customer_by_id) instantânea.
        st.session_state.customers = {
            1: {"id": 1, "nome": "Cliente Padrão", "email": "padrao@email.com", "telefone": "(11) 98765-4321", "endereco": "Rua A, 100"},
        }
    
    if "next_customer_id" not in st.session_state:
        # Controla qual será o próximo ID de cliente
        st.session_state.next_customer_id = 2 

def adicionar_cliente(nome, email, telefone, endereco):
    """
    Adiciona um novo cliente ao dicionário no st.session_state.
    """
    if not nome:
        st.error("Nome do cliente é obrigatório.")
        return None
    
    new_id = st.session_state.next_customer_id
    
    st.session_state.customers[new_id] = {
        "id": new_id,
        "nome": nome,
        "email": email,
        "telefone": telefone,
        "endereco": endereco
    }
    
    # Incrementa o ID para o próximo cadastro
    st.session_state.next_customer_id += 1
    st.toast(f"Cliente '{nome}' (ID: {new_id}) cadastrado!", icon="🎉")
    return new_id

def get_customers():
    """
    Retorna o dicionário completo de clientes.
    Usado pela interface de vendas (pag_venda) para listar o selectbox.
    """
    return st.session_state.customers

def get_customer_by_id(customer_id):
    """
    Busca um cliente específico pelo seu ID.
    
    !! ESTA É A FUNÇÃO CRUCIAL QUE SEU ARQUIVO pag_venda.py USA !!
    """
    # .get(customer_id) é a forma rápida de buscar em um dicionário
    return st.session_state.customers.get(customer_id) 

def remover_cliente(customer_id):
    """
    Remove um cliente do dicionário.
    """
    if customer_id in st.session_state.customers:
        # Não permite remover o cliente padrão (ID 1)
        if customer_id == 1:
            st.warning("Não é possível remover o 'Cliente Padrão'.")
            return False
            
        del st.session_state.customers[customer_id]
        st.toast(f"Cliente ID {customer_id} removido.", icon="🗑")
        return True
    return False

# ==============================================================================
# PARTE 2: INTERFACE DA PÁGINA (UI)
#
# Este é o código que o Streamlit executa quando o usuário
# clica na página "Gerenciar Clientes".
# ==============================================================================

# Garante que o session_state foi inicializado ANTES de tentar usá-lo
initialize_customers()

# --- Formulário para Adicionar Novo Cliente ---
st.subheader("Cadastrar Novo Cliente")
with st.form("form_cadastro_cliente", clear_on_submit=True):
    nome = st.text_input("Nome*")
    email = st.text_input("Email")
    telefone = st.text_input("Telefone")
    endereco = st.text_input("Endereço")
    
    # Botão de submit do formulário
    submitted = st.form_submit_button("Cadastrar Cliente")
    if submitted:
        # Chama a função de lógica (Parte 1) para adicionar o cliente
        adicionar_cliente(nome, email, telefone, endereco)

st.divider()

# --- Seção para Listar e Remover Clientes ---
st.subheader("Clientes Cadastrados")

# Pega o dicionário de clientes
customers_dict = get_customers()

if not customers_dict:
    st.info("Nenhum cliente cadastrado ainda.")
else:
    # Converte o dicionário para um DataFrame do Pandas para fácil visualização
    # 'orient="index"' usa as chaves do dicionário (os IDs) como linhas
    df = pd.DataFrame.from_dict(customers_dict, orient='index')
    
    # Reordena colunas para uma melhor visualização (opcional)
    try:
        df = df[["id", "nome", "email", "telefone", "endereco"]]
    except KeyError:
        pass # Ignora se alguma coluna não existir

    st.dataframe(df, use_container_width=True)

    # --- Seção de Remoção ---
    st.markdown("### Remover Cliente")
    
    # Cria uma lista de opções para o selectbox
    # (Ex: "Cliente Padrão (ID: 1)")
    options_dict = {cid: f"{c['nome']} (ID: {cid})" for cid, c in customers_dict.items()}
    
    id_to_remove = st.selectbox(
        "Selecione um cliente para remover",
        options=options_dict.keys(),
        format_func=lambda cid: options_dict[cid], # Mostra o texto formatado
        index=None,
        placeholder="Selecione..."
    )

    if st.button("Remover Cliente Selecionado", type="primary"):
        if id_to_remove:
            # Chama a função de lógica (Parte 1) para remover
            if remover_cliente(id_to_remove):
                st.rerun() # Atualiza a página para mostrar a lista sem o item
        else:
            st.warning("Nenhum cliente selecionado.")