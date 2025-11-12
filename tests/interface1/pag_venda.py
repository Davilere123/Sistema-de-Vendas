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

def add_to_cart(product_id, quantity=1):
    """Adiciona um item ao carrinho."""
    from product_manager import get_product_by_id # Importação local
    
    product = get_product_by_id(product_id)
    if product:
        if product_id in st.session_state.cart:
            st.session_state.cart[product_id] += quantity
        else:
            st.session_state.cart[product_id] = quantity
        st.toast(f"{product['name']} adicionado ao carrinho!", icon="➕")

def remove_from_cart(product_id):
    """Remove um item do carrinho."""
    if product_id in st.session_state.cart:
        del st.session_state.cart[product_id]

def get_cart_items():
    """Retorna os itens do carrinho com detalhes."""
    from product_manager import get_product_by_id # Importação local
    
    cart_items = []
    for product_id, quantity in st.session_state.cart.items():
        product = get_product_by_id(product_id)
        if product:
            subtotal = product["price"] * quantity
            cart_items.append({**product, "product_id": product_id, "quantity": quantity, "subtotal": subtotal})
    return cart_items

def calculate_cart_total():
    """Calcula o total do carrinho."""
    total = 0.0
    for item in get_cart_items():
        total += item["subtotal"]
    return total

def finalize_sale(customer_id):
    """Move o carrinho para o histórico de pedidos e o limpa."""
    from customer_manager import get_customer_by_id # Importação local
    
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