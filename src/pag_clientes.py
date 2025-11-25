import streamlit as st #importando o streamlit
import pandas as pd

# Textos explicativos --------------------
st.title("Gerenciamento de Clientes 👥")
st.header("Aqui você pode gerenciar seus clientes.")


class CustomerManager:
    """Gerencia clientes usando `st.session_state` como armazenamento.

    Esta classe encapsula toda a lógica (inicializar, adicionar,
    listar, buscar por ID e remover). Mantemos chamadas a `st` para
    exibir mensagens ao usuário quando apropriado.
    """

    def __init__(self, session_state=None):
        self.ss = session_state if session_state is not None else st.session_state

    def initialize(self):
        if "customers" not in self.ss:
            self.ss.customers = {
                1: {"id": 1, "nome": "Cliente Padrão", "email": "padrao@email.com", "telefone": "(11) 98765-4321", "endereco": "Rua A, 100"},
            }

        if "next_customer_id" not in self.ss:
            self.ss.next_customer_id = 2

    def add_customer(self, nome, email="", telefone="", endereco=""):
        if not nome:
            st.error("Nome do cliente é obrigatório.")
            return None

        new_id = self.ss.next_customer_id
        self.ss.customers[new_id] = {
            "id": new_id,
            "nome": nome,
            "email": email,
            "telefone": telefone,
            "endereco": endereco,
        }

        self.ss.next_customer_id += 1
        st.toast(f"Cliente '{nome}' (ID: {new_id}) cadastrado!", icon="🎉")
        return new_id

    def get_customers(self):
        return self.ss.customers

    def get_customer_by_id(self, customer_id):
        return self.ss.customers.get(customer_id)

    def remove_customer(self, customer_id):
        if customer_id in self.ss.customers:
            if customer_id == 1:
                st.warning("Não é possível remover o 'Cliente Padrão'.")
                return False
            del self.ss.customers[customer_id]
            st.toast(f"Cliente ID {customer_id} removido.", icon="🗑")
            return True
        return False


# Instância global (compatibilidade): outros módulos podem importar
# `customer_manager` ou usar os wrappers abaixo.
customer_manager = CustomerManager()


# Wrappers de nível de módulo para compatibilidade com código existente
def initialize_customers():
    return customer_manager.initialize()


def adicionar_cliente(nome, email, telefone, endereco):
    return customer_manager.add_customer(nome, email, telefone, endereco)


def get_customers():
    return customer_manager.get_customers()


def get_customer_by_id(customer_id):
    return customer_manager.get_customer_by_id(customer_id)


def remover_cliente(customer_id):
    return customer_manager.remove_customer(customer_id)


# ======================================================================
# PARTE 2: INTERFACE DA PÁGINA (UI)
#
# O código abaixo monta a interface do Streamlit. Mantivemos a lógica
# separada na classe e usamos os wrappers para simplicidade e compatibilidade.
# ======================================================================

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
            if remover_cliente(id_to_remove):
                st.rerun() # Atualiza a página para mostrar a lista sem o item
        else:
            st.warning("Nenhum cliente selecionado.")
