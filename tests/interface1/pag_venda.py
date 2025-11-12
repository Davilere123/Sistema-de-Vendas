import streamlit as st
import datetime
#Textos explicativos --------------------
st.title("Vendas 🛒")
st.header("Aqui você pode gerenciar suas vendas.")
st.write("Funcionalidades de vendas serão implementadas em breve.")

def initialize_sales():
    """Inicializa o carrinho e o histórico de pedidos."""
    if "cart" not in st.session_state:
        st.session_state.cart = {} # {product_id: quantity}
    if "orders" not in st.session_state:
        st.session_state.orders = [] # Lista de pedidos finalizados

def add_to_cart(product_name, quantity=1):
    """Adiciona um item ao carrinho."""
    from pag_produtos import get_product_by_name # Importação local
    
    product = get_product_by_name(product_name)
    if product:
        if product_name in st.session_state.cart:
            st.session_state.cart[product_name] += quantity
        else:
            st.session_state.cart[product_name] = quantity
        st.toast(f"{product['Nome']} adicionado ao carrinho!", icon="➕")

def remove_from_cart(product_name):
    """Remove um item do carrinho."""
    if product_name in st.session_state.cart:
        del st.session_state.cart[product_name]

def get_cart_items():
    """Retorna os itens do carrinho com detalhes."""
    from pag_produtos import get_product_by_name # Importação local
    
    cart_items = []
    for product_name, quantity in st.session_state.cart.items():
        product = get_product_by_name(product_name)
        if product:
            subtotal = product["Preço"] * quantity
            cart_items.append({**product, "product_name": product_name, "quantity": quantity, "subtotal": subtotal})
    return cart_items

def calculate_cart_total():
    """Calcula o total do carrinho."""
    total = 0.0
    for item in get_cart_items():
        total += item["subtotal"]
    return total

def finalize_sale(customer_id):
    """Move o carrinho para o histórico de pedidos e o limpa."""
    from pag_clientes import get_customer_by_id # Importação local
    
    cart_items = get_cart_items()
    total = calculate_cart_total()
    customer = get_customer_by_id(customer_id)
    
    if not cart_items:
        st.error("O carrinho está vazio.")
        return None

    order = {
        "order_id": f"PEDIDO_{len(st.session_state.orders) + 1:04d}",
        "customer": customer,
        "items": cart_items,
        "total": total,
        "date": datetime.datetime.now()
    }
    
    st.session_state.orders.append(order)
    st.session_state.cart.clear() # Limpa o carrinho
    
    st.success(f"Venda {order['order_id']} finalizada com sucesso!")
    return order