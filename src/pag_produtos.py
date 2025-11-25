import streamlit as st
from dataclasses import dataclass, asdict
from typing import List, Optional


@dataclass
class Produto:
    """Modelo simples de produto."""
    nome: str
    preco: float
    quantidade: int

    def to_dict(self) -> dict:
        return {"Nome": self.nome, "Preço": self.preco, "Quantidade": self.quantidade}


class ProdutoManager:
    """Gerencia produtos armazenados em `st.session_state` e renderiza a UI."""

    def __init__(self, session_state: Optional[object] = None):
        self.state = session_state if session_state is not None else st.session_state
        if "produtos" not in self.state:
            self.state.produtos = []

    # --- CRUD básico ---
    def add_produto(self, produto: Produto) -> None:
        self.state.produtos.append(produto.to_dict())

    def remove_produto_por_nome(self, nome: str) -> None:
        self.state.produtos = [p for p in self.state.produtos if p.get("Nome") != nome]

    def listar_produtos(self) -> List[dict]:
        return list(self.state.produtos)

    # --- Renderização/integração com Streamlit ---
    def render_header(self) -> None:
        st.title("Gerenciamento de produtos 📦")
        st.header("Aqui você pode gerenciar seus produtos.")

    def render_form_cadastro(self, form_key: str = "form_cadastro") -> None:
        st.subheader("🛒 Cadastro de Produtos")
        with st.form(form_key):
            nome = st.text_input("Nome do Produto")
            preco = st.number_input("Preço (R$)", min_value=0.0, format="%.2f")
            quantidade = st.number_input("Quantidade de Produtos", min_value=0, step=1)
            enviar = st.form_submit_button("Cadastrar")

            if enviar:
                if nome:
                    novo = Produto(nome=nome, preco=float(preco), quantidade=int(quantidade))
                    self.add_produto(novo)
                    st.success(f"✅ Produto '{nome}' cadastrado com sucesso!")
                else:
                    st.warning("⚠️ O nome do produto é obrigatório!")

    def render_lista(self) -> None:
        st.subheader("📋 Produtos cadastrados")
        produtos = self.listar_produtos()
        if produtos:
            st.table(produtos)
        else:
            st.info("Nenhum produto cadastrado ainda.")

    def render_remocao(self) -> None:
        st.subheader("🗑️ Remover Produtos")
        produtos = self.listar_produtos()
        if produtos:
            nomes = [p.get("Nome") for p in produtos]
            produto_remover = st.selectbox("Selecione o produto para remover", nomes)
            if st.button("Remover"):
                self.remove_produto_por_nome(produto_remover)
                st.success(f"Produto '{produto_remover}' removido!")
        else:
            st.write("Nenhum produto disponível para remover.")

    def render(self) -> None:
        """Renderiza toda a página de produtos."""
        self.render_header()
        self.render_form_cadastro()
        self.render_lista()
        self.render_remocao()


def render_page(session_state: Optional[object] = None) -> ProdutoManager:
    """Função de integração para outros módulos. Retorna o manager criado.

    Exemplo de uso em outro módulo:
        from src.pag_produtos import render_page
        render_page()
    """
    manager = ProdutoManager(session_state=session_state)
    manager.render()
    return manager


__all__ = ["Produto", "ProdutoManager", "render_page"]


if __name__ == "__main__":
    render_page()