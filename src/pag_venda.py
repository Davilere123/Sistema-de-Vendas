import streamlit as st
from dataclasses import dataclass, asdict
from typing import List, Optional
import datetime
import pandas as pd

# Integração com os módulos existentes (clientes/produtos/relatório)
import pag_clientes as pag_clientes
import pag_produtos as pag_produtos
import pag_relatorio as pag_relatorio

# ------------------ Item da Venda ----------------------
@dataclass
class CartItem:
    nome: str
    preco: float
    quantidade: int

    def subtotal(self) -> float:
        # Calcula subtotal do item (preço * quantidade)
        return float(self.preco) * int(self.quantidade)

#------------------ Carrinho -----------------------
class Cart:
    def __init__(self, session_state=None):
        # Usa o session_state para armazenar o carrinho
        self.ss = session_state if session_state is not None else st.session_state
        if "cart" not in self.ss:
            self.ss.cart = {}  # Armazena: nome do produto -> quantidade

    def add(self, nome: str, preco: float, quantidade: int = 1):
        # Adiciona itens ao carrinho (acumula se já existir)
        if nome in self.ss.cart:
            self.ss.cart[nome] += quantidade
        else:
            self.ss.cart[nome] = quantidade

    def remove(self, nome: str):
        # Remove produto do carrinho
        if nome in self.ss.cart:
            del self.ss.cart[nome]

    def clear(self):
        # Esvazia totalmente o carrinho
        self.ss.cart = {}

    def items(self) -> List[CartItem]:
        # Converte dados do carrinho em objetos CartItem
        items: List[CartItem] = []
        produtos = get_products_list()
        prod_by_name = {p.get("Nome"): p for p in produtos}
        for nome, qtd in self.ss.cart.items():
            p = prod_by_name.get(nome, {})
            preco = p.get("Preço", 0.0)
            items.append(CartItem(nome=nome, preco=preco, quantidade=int(qtd)))
        return items

    def total(self) -> float:
        # Soma os subtotais para obter o total da compra
        return sum(i.subtotal() for i in self.items())

#------------------ Gerenciador de Vendas ----------------------
class SaleManager:
    def __init__(self, session_state=None):
        # Gerencia vendas, carrinho e IDs das vendas
        self.ss = session_state if session_state is not None else st.session_state
        if "sales" not in self.ss:
            self.ss.sales = []  # Lista de vendas realizadas
        if "next_sale_id" not in self.ss:
            self.ss.next_sale_id = 1  # Controle do ID da próxima venda
        self.cart = Cart(self.ss)

    def initialize(self):
        # Inicializa clientes e produtos, caso os módulos tenham essas funções
        if pag_clientes and hasattr(pag_clientes, "initialize_customers"):
            pag_clientes.initialize_customers()
        if pag_produtos and hasattr(pag_produtos, "ProdutoManager"):
            pag_produtos.ProdutoManager(session_state=self.ss)

    def add_product_to_cart(self, product_name: str, quantidade: int = 1) -> bool:
        # Adiciona produto ao carrinho verificando estoque
        produtos = get_products_list()
        prod = next((p for p in produtos if p.get("Nome") == product_name), None)
        if not prod:
            st.error("Produto não encontrado.")
            return False
        estoque = int(prod.get("Quantidade", 0))
        if estoque < quantidade:
            st.warning(f"Estoque insuficiente para '{product_name}'. Estoque: {estoque}")
            return False
        self.cart.add(product_name, float(prod.get("Preço", 0.0)), quantidade)
        st.toast(f"{product_name} adicionado ao carrinho", icon="➕")
        return True

    def remove_product_from_cart(self, product_name: str):
        # Remove item do carrinho e exibe toast
        self.cart.remove(product_name)
        st.toast("Item removido do carrinho", icon="🗑️")

    def finalize_sale(self, customer_id: int) -> Optional[dict]:
        # Finaliza a venda: valida cliente, carrinho e diminui estoque
        customers = get_customers_dict()
        customer = customers.get(customer_id)
        if not customer:
            st.error("Cliente não encontrado.")
            return None

        items = self.cart.items()
        if not items:
            st.error("O carrinho está vazio.")
            return None

        # Reduz o estoque dos produtos vendidos
        for item in items:
            if not decrement_product_stock(item.nome, item.quantidade):
                st.error(f"Falha ao decrementar estoque de {item.nome}.")
                return None

        # Monta o objeto da venda
        sale = {
            "id": int(self.ss.next_sale_id),
            "customer": customer,
            "items": [asdict(i) for i in items],
            "total": float(self.cart.total()),
            "date": datetime.datetime.now(),
        }

        # Salva a venda
        self.ss.sales.append(sale)
        self.ss.next_sale_id += 1
        self.cart.clear()
        st.success(f"Venda {sale['id']} finalizada com sucesso!")
        return sale

    def list_sales(self) -> List[dict]:
        # Retorna lista de vendas registradas
        return list(self.ss.sales)


# ------------------ Helpers para integração ------------------
def get_products_list() -> List[dict]:
    # Usa o ProdutoManager se existir, senão usa session_state diretamente
    if pag_produtos and hasattr(pag_produtos, "ProdutoManager"):
        mgr = pag_produtos.ProdutoManager(session_state=st.session_state)
        return mgr.listar_produtos()
    return list(st.session_state.get("produtos", []))


def decrement_product_stock(nome: str, quantidade: int) -> bool:
    # Reduz estoque de um produto após a venda
    produtos = st.session_state.get("produtos", None)
    if produtos is None and pag_produtos and hasattr(pag_produtos, "ProdutoManager"):
        pag_produtos.ProdutoManager(session_state=st.session_state)
        produtos = st.session_state.get("produtos", [])

    for p in produtos:
        if p.get("Nome") == nome:
            estoque = int(p.get("Quantidade", 0))
            if estoque < quantidade:
                return False
            p["Quantidade"] = estoque - int(quantidade)
            return True
    return False


def get_customers_dict() -> dict:
    # Retorna dict de clientes cadastrados
    if pag_clientes and hasattr(pag_clientes, "get_customers"):
        return pag_clientes.get_customers()
    return getattr(st.session_state, "customers", {})


# ------------------ UI / Render ------------------
def render_page(session_state: Optional[object] = None) -> SaleManager:
    # Renderiza interface da página de vendas
    ss = session_state if session_state is not None else st.session_state
    manager = SaleManager(session_state=ss)
    manager.initialize()

    st.title("Vendas 🛒")
    st.header("Faça vendas - adicione itens ao carrinho e finalize.")

    cols = st.columns([2, 1])

    # Lado esquerdo: catálogo de produtos
    with cols[0]:
        st.subheader("Produtos Disponíveis")
        produtos = get_products_list()
        if not produtos:
            st.info("Nenhum produto cadastrado.")
        else:
            cols_prod = st.columns(3)
            for i, p in enumerate(produtos):
                with cols_prod[i % 3]:
                    nome = p.get("Nome")
                    preco = p.get("Preço", 0.0)
                    estoque = p.get("Quantidade", 0)
                    st.markdown(f"**{nome}**")
                    st.write(f"R$ {preco:.2f} — Estoque: {estoque}")
                    # Seleciona quantidade
                    qtd = st.number_input(f"Qtd ({nome})", min_value=1, max_value=max(1, int(estoque)), value=1, key=f"qtd_{nome}")
                    if st.button("Adicionar", key=f"add_{nome}"):
                        manager.add_product_to_cart(nome, int(qtd))

    # Lado direito: carrinho e checkout
    with cols[1]:
        st.subheader("Carrinho")
        items = manager.cart.items()
        if not items:
            st.info("Carrinho vazio.")
        else:
            for it in items:
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.write(f"{it.quantidade}x {it.nome} — R$ {it.subtotal():.2f}")
                with c2:
                    if st.button("Remover", key=f"rm_{it.nome}"):
                        manager.remove_product_from_cart(it.nome)

            st.divider()
            st.markdown(f"**Total: R$ {manager.cart.total():.2f}**")

            # Seleção de cliente
            customers = get_customers_dict()
            if customers:
                options = list(customers.keys())
                selected = st.selectbox("Selecione Cliente", options=options, format_func=lambda cid: customers[cid]["nome"]) 
            else:
                selected = None
                st.info("Nenhum cliente cadastrado. Cadastre clientes antes de finalizar.")

            # Botão finalizar venda
            if st.button("Finalizar Venda", type="primary"):
                if not selected:
                    st.error("Selecione um cliente antes de finalizar a venda.")
                else:
                    sale = manager.finalize_sale(selected)
                    # Gera PDF se o módulo de relatório permitir
                    if sale and pag_relatorio and hasattr(pag_relatorio, "generate_sale_pdf"):
                        pdf = pag_relatorio.generate_sale_pdf(sale)
                        st.download_button(label="Baixar Recibo PDF", data=pdf, file_name=f"sale_{sale['id']}.pdf", mime="application/pdf")

    return manager


if __name__ == "__main__":
    render_page()
