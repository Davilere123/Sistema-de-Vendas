import streamlit as st
import datetime
import importlib

# Tenta importar módulos de interface (podem ser apenas páginas sem funções).
try:
    cm = importlib.import_module('tests.interface1.pag_clientes')
except Exception:
    try:
        cm = importlib.import_module('pag_clientes')
    except Exception:
        cm = None

try:
    pm = importlib.import_module('tests.interface1.pag_produtos')
except Exception:
    try:
        pm = importlib.import_module('pag_produtos')
    except Exception:
        pm = None

try:
    rg = importlib.import_module('tests.interface1.pag_relatorio')
except Exception:
    try:
        rg = importlib.import_module('pag_relatorio')
    except Exception:
        rg = None

try:
    # fallback para pegar catálogo em src/app.py
    app_src = importlib.import_module('src.app')
except Exception:
    app_src = None


# --- INICIALIZAÇÃO DO ESTADO DA SESSÃO ---
def initialize_sales():
    """Inicializa o carrinho, catálogo e clientes na sessão."""
    if 'cart' not in st.session_state:
        st.session_state.cart = {}  # {product_key: quantity}
    if 'orders' not in st.session_state:
        st.session_state.orders = []

    # Inicializa produtos: tenta usar o módulo de produtos, senão usa src.app.PRODUCTS
    if 'products' not in st.session_state:
        products = {}
        if pm and hasattr(pm, 'get_all_products'):
            try:
                for p in pm.get_all_products():
                    # espera dicionário com Nome/Preço/icon/estoque
                    key = p.get('Nome') or p.get('name')
                    products[key] = p
            except Exception:
                products = {}
        elif app_src and hasattr(app_src, 'PRODUCTS'):
            for k, v in getattr(app_src, 'PRODUCTS').items():
                # Mapeia para formato esperado
                name = v.get('name')
                products[name] = {
                    'key': k,
                    'Nome': name,
                    'Preço': v.get('price', 0.0),
                    'icon': v.get('image', '📦'),
                    'estoque': 100
                }
        else:
            # Catálogo mínimo de fallback
            products = {
                'Hambúrguer': {'Nome': 'Hambúrguer', 'Preço': 25.50, 'icon': '🍔', 'estoque': 20},
                'Pizza': {'Nome': 'Pizza', 'Preço': 42.00, 'icon': '🍕', 'estoque': 10},
            }
        st.session_state.products = products

    # Histórico de ações para permitir 'desfazer'
    if 'last_actions' not in st.session_state:
        st.session_state.last_actions = []  # lista de tuples (action, product_key, quantity)

    # Inicializa clientes (se módulo de clientes fornecer função usa, senão cria fallback)
    if 'customers' not in st.session_state:
        customers = {}
        if cm and hasattr(cm, 'get_customers'):
            try:
                customers = cm.get_customers()
            except Exception:
                customers = {}
        if not customers:
            customers = {
                'cli_001': {'nome': 'Cliente Exemplo', 'cpf': '000.000.000-00'},
                'cli_002': {'nome': 'Outro Cliente', 'cpf': '111.111.111-11'},
            }
        st.session_state.customers = customers


# --- MANIPULAÇÃO DO CARRINHO ---
def add_to_cart(product_key, quantity=1):
    """Adiciona um item ao carrinho (usa chave do produto como identificador)."""
    products = st.session_state.get('products', {})
    prod = products.get(product_key)
    if not prod:
        # tenta procurar por nome similar
        for k, v in products.items():
            if k == product_key or v.get('Nome') == product_key:
                prod = v
                product_key = k
                break

    if not prod:
        st.error('Produto não encontrado')
        return False

    estoque = prod.get('estoque')
    if estoque is not None and estoque < quantity:
        st.error(f"Estoque insuficiente para {prod.get('Nome')}. Disponível: {estoque}")
        return False

    st.session_state.cart[product_key] = st.session_state.cart.get(product_key, 0) + quantity
    if estoque is not None:
        prod['estoque'] = estoque - quantity
    # registra ação para desfazer
    st.session_state.last_actions.append(('add', product_key, quantity))
    try:
        st.toast(f"{prod.get('Nome')} adicionado ao carrinho!", icon='➕')
    except Exception:
        st.success(f"{prod.get('Nome')} adicionado ao carrinho!")
    return True


def remove_from_cart(product_key):
    """Remove item do carrinho e restaura o estoque."""
    if product_key not in st.session_state.cart:
        return False
    qty = st.session_state.cart[product_key]
    prod = st.session_state.products.get(product_key)
    if prod and prod.get('estoque') is not None:
        prod['estoque'] = prod.get('estoque', 0) + qty
    # registra ação para desfazer (remoção total)
    st.session_state.last_actions.append(('remove', product_key, qty))
    del st.session_state.cart[product_key]
    try:
        st.toast('Item removido.', icon='🗑️')
    except Exception:
        st.info('Item removido.')
    return True


def get_cart_items():
    items = []
    for key, qty in st.session_state.cart.items():
        prod = st.session_state.products.get(key)
        if not prod:
            # tenta por nome
            for k, v in st.session_state.products.items():
                if k == key or v.get('Nome') == key:
                    prod = v
                    break
        if not prod:
            continue
        subtotal = prod.get('Preço', 0.0) * qty
        item = {
            'product_id': key,
            'Nome': prod.get('Nome'),
            'quantity': qty,
            'Preço': prod.get('Preço', 0.0),
            'subtotal': subtotal
        }
        items.append(item)
    return items


def calculate_cart_total():
    total = 0.0
    for it in get_cart_items():
        total += it['subtotal']
    return total


def finalize_sale(customer_id):
    customers = st.session_state.get('customers', {})
    customer = customers.get(customer_id)
    if not customer:
        st.error('Cliente não encontrado')
        return None

    items = get_cart_items()
    if not items:
        st.error('Carrinho vazio')
        return None

    total = calculate_cart_total()
    order = {
        'order_id': f"PEDIDO_{len(st.session_state.orders)+1:04d}",
        'customer': customer,
        'items': items,
        'total': total,
        'date': datetime.datetime.now()
    }
    st.session_state.orders.append(order)
    st.session_state.cart = {}
    st.session_state.last_actions = []
    st.success(f"Venda {order['order_id']} finalizada com sucesso!")
    return order


# --- Título e Cabeçalho ---
st.title('Vendas 🛒')
st.header('Gerencie suas vendas aqui')

# Link de voltar (usa histórico do navegador). Funciona quando abriu via outra página.
st.markdown("<a href='javascript:history.back()'>&larr; Voltar</a>", unsafe_allow_html=True)

# Inicializa dados
initialize_sales()

# Layout com duas colunas
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader('Produtos Disponíveis')
    products = list(st.session_state.get('products', {}).values())
    if not products:
        st.info('Nenhum produto disponível')
    else:
        cols = st.columns(3)
        idx = 0
        for prod in products:
            with cols[idx]:
                st.markdown(f"**{prod.get('icon', '📦')} {prod.get('Nome')}**")
                st.write(f"R$ {prod.get('Preço', 0.0):.2f}")
                estoque = prod.get('estoque')
                if estoque is not None:
                    st.caption(f"Estoque: {estoque}")
                key = prod.get('Nome')
                if st.button('Adicionar', key=f"add_{key}"):
                    add_to_cart(key, 1)
                    # Não forçamos rerun; Streamlit re-executa automaticamente após interação
            idx = (idx + 1) % 3

with col2:
    st.subheader('Carrinho')
    cart_items = get_cart_items()
    if not cart_items:
        st.info('Carrinho vazio')
    else:
        for it in cart_items:
            # cria colunas internas para -, + e descrição
            col_minus, col_plus, col_desc, col_remove = st.columns([1,1,6,1])
            with col_minus:
                if st.button('-', key=f"minus_{it['product_id']}"):
                    # decrementar uma unidade
                    pid = it['product_id']
                    current = st.session_state.cart.get(pid, 0)
                    if current > 1:
                        st.session_state.cart[pid] = current - 1
                        # restaura 1 no estoque
                        prod = st.session_state.products.get(pid)
                        if prod and prod.get('estoque') is not None:
                            prod['estoque'] += 1
                        st.session_state.last_actions.append(('remove_one', pid, 1))
                    else:
                        # remove completamente
                        remove_from_cart(pid)
                    # rely on Streamlit automatic rerun
            with col_plus:
                if st.button('+', key=f"plus_{it['product_id']}"):
                    add_to_cart(it['product_id'], 1)
                    # rely on Streamlit automatic rerun
            with col_desc:
                st.write(f"{it['quantity']}x {it['Nome']} — R$ {it['subtotal']:.2f}")
            with col_remove:
                if st.button('Rem', key=f"rem_{it['product_id']}"):
                    remove_from_cart(it['product_id'])
                    # rely on Streamlit automatic rerun

        st.divider()
        total = calculate_cart_total()
        st.markdown(f"### Total: R$ {total:.2f}")

        st.divider()
        # ações adicionais: desfazer último e limpar carrinho
        col_action_1, col_action_2 = st.columns([1,1])
        with col_action_1:
            if st.button('Desfazer último'):
                # desfaz a última ação
                if st.session_state.last_actions:
                    act, pid, q = st.session_state.last_actions.pop()
                    if act == 'add':
                        # remove q do carrinho e devolve ao estoque
                        cur = st.session_state.cart.get(pid, 0)
                        remove_q = min(q, cur)
                        if remove_q > 0:
                            st.session_state.cart[pid] = cur - remove_q
                            if st.session_state.cart[pid] <= 0:
                                del st.session_state.cart[pid]
                            prod = st.session_state.products.get(pid)
                            if prod and prod.get('estoque') is not None:
                                prod['estoque'] += remove_q
                    elif act == 'remove':
                        # re-adiciona q ao carrinho (tenta debitar estoque)
                        prod = st.session_state.products.get(pid)
                        available = prod.get('estoque') if prod else None
                        addable = q if (available is None or available >= q) else available
                        if addable > 0:
                            st.session_state.cart[pid] = st.session_state.cart.get(pid, 0) + addable
                            if prod and prod.get('estoque') is not None:
                                prod['estoque'] -= addable
                    elif act == 'remove_one':
                        # re-adiciona 1 unidade
                        st.session_state.cart[pid] = st.session_state.cart.get(pid, 0) + q
                        prod = st.session_state.products.get(pid)
                        if prod and prod.get('estoque') is not None:
                            prod['estoque'] -= q
                    
                else:
                    st.info('Nada para desfazer')
        with col_action_2:
            if st.button('Limpar carrinho'):
                # restaura estoques e limpa
                for pid, qty in list(st.session_state.cart.items()):
                    prod = st.session_state.products.get(pid)
                    if prod and prod.get('estoque') is not None:
                        prod['estoque'] += qty
                st.session_state.cart = {}
                st.session_state.last_actions = []
                # rely on Streamlit automatic rerun
        customers = st.session_state.get('customers', {})
        selected = None
        if customers:
            options = list(customers.keys())
            selected = st.selectbox('Selecione o cliente', options, format_func=lambda cid: customers[cid].get('nome'))

        if st.button('Finalizar Venda', type='primary'):
            if not selected:
                st.error('Selecione um cliente')
            else:
                order = finalize_sale(selected)
                if order:
                    # tenta gerar PDF via módulo de relatório
                    pdf_bytes = None
                    if rg and hasattr(rg, 'generate_sale_pdf'):
                        try:
                            pdf_bytes = rg.generate_sale_pdf(order)
                        except Exception:
                            pdf_bytes = None
                    if pdf_bytes:
                        st.download_button('Baixar Recibo PDF', data=pdf_bytes, file_name=f"{order['order_id']}_recibo.pdf", mime='application/pdf')
                    else:
                        st.info('Recibo disponível na lista de pedidos (sem PDF).')