import streamlit as st
import datetime
# Importações de módulos do projeto (product_manager, customer_manager)
# serão feitas DENTRO das funções para evitar Importação Circular.
#Textos explicativos --------------------
st.title("Vendas 🛒")
st.header("Aqui você pode gerenciar suas vendas.")

# --- INICIALIZAÇÃO DO ESTADO DA SESSÃO ---
def initialize_sales():
    """Inicializa o carrinho e o histórico de pedidos."""
    if "cart" not in st.session_state:
        st.session_state.cart = {} # {product_id: quantity}
        st.session_state.cart = {} # {product_name: quantity}
    if "orders" not in st.session_state:
        st.session_state.orders = [] # Lista de pedidos finalizados

# --- MANIPULAÇÃO DO CARRINHO ---
def add_to_cart(product_name, quantity=1):
    """Adiciona um item ao carrinho."""
    from pag_produtos import get_product_by_name # Importação local: Evita erros de "Importação Circular".
    # Pede ao "gerente de produtos" os detalhes deste item.

    product = get_product_by_name(product_name)
    # Garante que o produto existe no catálogo antes de adicionar
    if product:
        # Verifica se o produto já está no carrinho
        if product_name in st.session_state.cart:
            # Se sim, apenas soma a quantidade
            st.session_state.cart[product_name] += quantity
        else:
            # Se não, adiciona a nova entrada no dicionário
            st.session_state.cart[product_name] = quantity
            
        # Fornece feedback visual ao usuário (toast)
        # Usa a chave "Nome" (Português) vinda do product_manager
        st.toast(f"{product['Nome']} adicionado ao carrinho!", icon="➕")

def remove_from_cart(product_name):
    """Remove um item do carrinho."""
    # Verifica se a chave (nome do produto) existe no dicionário do carrinho
    if product_name in st.session_state.cart:
        # 'del' é o comando Python para remover uma chave de um dicionário
        del st.session_state.cart[product_name]
        st.toast("Item removido.", icon="🗑️")

def get_cart_items():
    """Retorna os itens do carrinho com detalhes."""
    from pag_produtos import get_product_by_name # Importação local

    cart_items = []
    # Itera sobre o dicionário do carrinho (item por item)
    for product_name, quantity in st.session_state.cart.items():
        
        # Pede os detalhes do produto ao gerente de produtos
        product = get_product_by_name(product_name)
        if product:
            # Calcula o subtotal (preço x quantidade)
            subtotal = product["Preço"] * quantity
            item_detalhado = {
                **product,  # Copia todas as chaves de 'product' (Nome, Preço, etc.)
                "product_id": product_name, # Salva o nome como o ID
                "quantity": quantity,
                "subtotal": subtotal
            }
            cart_items.append(item_detalhado)
    return cart_items

def calculate_cart_total():
    """Calcula o total do carrinho."""
    total = 0.0
    
    # Pega a lista detalhada de itens (que já tem o subtotal)
    items = get_cart_items()
    
    # Apenas soma o subtotal de cada item
    for item in items:
        total += item["subtotal"]
        
    return total

def finalize_sale(customer_id):
    """Move o carrinho para o histórico de pedidos e o limpa."""
    from pag_clientes import get_customer_by_id # Importação local

    # Reunião de Dados
    cart_items = get_cart_items() # Pega os itens detalhados
    total = calculate_cart_total() # Calcula o total
    customer = get_customer_by_id(customer_id) # Pega os dados do cliente

    # Validação
    # Impede a finalização de um carrinho vazio
    if not cart_items:
        st.error("O carrinho está vazio.")
        return None
        
    if not customer:
        st.error("Cliente não encontrado.")
        return None
    
    # Criação do Pedido
    # Monta o "recibo" final (um dicionário com tudo)
    order = {
        "order_id": f"PEDIDO_{len(st.session_state.orders) + 1:04d}",
        "customer": customer, # Dicionário com dados do cliente
        "items": cart_items,  # Lista de dicionários dos itens
        "total": total,
        "date": datetime.datetime.now() # Registra data e hora exatas
    }

    # Adiciona o pedido recém-criado ao histórico
    st.session_state.orders.append(order)
    
    # Limpa o carrinho para a próxima venda
    st.session_state.cart.clear()

    st.success(f"Venda {order['order_id']} finalizada com sucesso!")
    
    # Retorna o recibo (order) para a interface
    # A interface vai usar isso para gerar o PDF.
    return order