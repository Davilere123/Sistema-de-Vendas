import streamlit as st
import pandas as pd
import datetime
import base64
from typing import List, Optional
# Importa o gerador de PDF
from fpdf import FPDF 

# ----------------------------------------------------
# CLASSE PRINCIPAL (Modelada a partir de SaleManager)
# ----------------------------------------------------

class RelatorioManager:
    """
    Gerencia a lógica de acesso a dados de vendas e geração de relatórios.
    Assume que as vendas estão armazenadas em st.session_state.sales.
    """
    def __init__(self, session_state=None):
        # Inicializa com st.session_state se nenhum estado for fornecido
        self.ss = session_state if session_state is not None else st.session_state
        # Garante que 'sales' existe para evitar erros
        if "sales" not in self.ss:
            self.ss.sales = []

    def get_sales_dataframe(self, days: int = 30) -> pd.DataFrame:
        """
        Converte a lista de vendas em st.session_state para um DataFrame, 
        e filtra pelos últimos 'days' dias.
        """
        sales_list = self.ss.get("sales", [])
        
        if not sales_list:
            return pd.DataFrame()

        # Normaliza a lista de dicionários para um DataFrame
        df = pd.DataFrame(sales_list)
        df["date"] = pd.to_datetime(df["date"])
        
        hoje = datetime.datetime.now()
        data_limite = hoje - pd.Timedelta(days=days)
        
        # Filtra as vendas
        vendas_filtradas = df[df["date"] > data_limite]
        
        # Renomeia colunas para o contexto do relatório
        vendas_filtradas = vendas_filtradas.rename(
            columns={"total": "valor_venda", "date": "data_venda"}
        )
        
        # Cria uma coluna de quantidade total de itens (se necessário para o relatório)
        # O total de itens precisa ser calculado a partir da lista 'items' dentro de cada venda.
        vendas_filtradas["quantidade"] = vendas_filtradas["items"].apply(
            lambda items: sum(i.get("quantidade", 0) for i in items)
        )
        
        return vendas_filtradas
    
# ----------------------------------------------------
# HELPERS / FUNÇÕES DE INTEGRAÇÃO (Como as do primeiro código)
# ----------------------------------------------------

def get_sales_list() -> List[dict]:
    """Retorna a lista de vendas do session_state, alinhado aos helpers do pag_vendas."""
    return list(st.session_state.get("sales", []))

def generate_sale_pdf(sale: dict) -> bytes:
    """
    Gera um PDF para uma única venda finalizada.
    Essa função é chamada pelo SaleManager (pag_vendas) após finalizar a venda.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    
    # Título do Recibo
    pdf.cell(0, 15, f"Recibo de Venda #{sale['id']}", ln=True, align="C")
    pdf.ln(5)

    # Detalhes da Venda
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, f"Cliente: {sale['customer']['nome']}", ln=True)
    pdf.cell(0, 8, f"Data: {sale['date'].strftime('%d/%m/%Y %H:%M:%S')}", ln=True)
    pdf.ln(5)

    # Detalhes dos Itens
    pdf.set_font("Arial", "B", 12)
    pdf.cell(10, 8, "Qtde", border=1)
    pdf.cell(80, 8, "Produto", border=1)
    pdf.cell(40, 8, "Preço Unitário", border=1)
    pdf.cell(40, 8, "Subtotal", border=1, ln=True)
    
    pdf.set_font("Arial", size=12)
    for item in sale["items"]:
        subtotal = float(item["preco"]) * int(item["quantidade"])
        pdf.cell(10, 8, str(item["quantidade"]), border=1)
        pdf.cell(80, 8, item["nome"], border=1)
        pdf.cell(40, 8, f"R$ {item['preco']:.2f}", border=1)
        pdf.cell(40, 8, f"R$ {subtotal:.2f}", border=1, ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"TOTAL GERAL: R$ {sale['total']:.2f}", ln=True, align="R")

    # Retorna o conteúdo binário do PDF
    return pdf.output(dest="S").encode("latin-1")

# ----------------------------------------------------
# UI / RENDER (Função de renderização da página de relatório)
# ----------------------------------------------------

def render_page(session_state: Optional[object] = None) -> RelatorioManager:
    """
    Renderiza a interface da página de Relatórios.
    """
    ss = session_state if session_state is not None else st.session_state
    manager = RelatorioManager(session_state=ss)

    st.title("Relatório de Vendas")
    st.header("Análise das Vendas Registradas")

    # Obtém os dados de vendas
    days_filter = st.slider("Filtrar vendas pelos últimos N dias:", min_value=1, max_value=365, value=30)
    vendas_df = manager.get_sales_dataframe(days=days_filter)

    if vendas_df.empty:
        st.info("Nenhuma venda registrada no período selecionado.")
        return manager

    # Calcular resumo
    total_vendas = vendas_df["valor_venda"].sum()
    quantidade_vendida = vendas_df["quantidade"].sum()
    data_limite = vendas_df["data_venda"].min()
    hoje = vendas_df["data_venda"].max()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Vendido", f"R$ {total_vendas:,.2f}")
    with col2:
        st.metric("Total de Itens", f"{quantidade_vendida}")
        
    st.divider()
    st.markdown(f"**Período analisado:** {data_limite.strftime('%d/%m/%Y')} até {hoje.strftime('%d/%m/%Y')}")
    st.dataframe(vendas_df[["id", "customer", "valor_venda", "quantidade", "data_venda"]])

    if st.button("Gerar Relatório de Análise (PDF)", type="primary"):
        # Lógica de geração do PDF de ANÁLISE (adaptada do seu segundo código)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, f"Relatório de Vendas - Últimos {days_filter} dias", ln=True, align="C")
        pdf.ln(10)
        
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Período: {data_limite.strftime('%d/%m/%Y')} até {hoje.strftime('%d/%m/%Y')}", ln=True)
        pdf.cell(0, 10, f"Total vendido: R$ {total_vendas:,.2f}", ln=True)
        pdf.cell(0, 10, f"Quantidade vendida: {quantidade_vendida}", ln=True)
        pdf.ln(10)
        
        pdf.cell(0, 10, "Detalhes das vendas (Top 10):", ln=True)
        pdf.ln(5)
        
        # Listagem das vendas (limitada a 10 para exemplo)
        for _, row in vendas_df.sort_values(by="data_venda", ascending=False).head(10).iterrows():
            pdf.cell(0, 7, f"Venda {row['id']} - {row['data_venda'].strftime('%d/%m/%Y')}: R$ {row['valor_venda']:.2f} (Cliente: {row['customer'].get('nome', 'N/A')})", ln=True)

        pdf_output = pdf.output(dest="S").encode("latin-1")

        # Criar link para download
        b64 = base64.b64encode(pdf_output).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="relatorio_vendas_{days_filter}dias.pdf">Clique aqui para baixar o PDF</a>'
        st.markdown(href, unsafe_allow_html=True)
    
    return manager

if __name__ == "__main__":
    # Inicializa st.session_state.sales para que o manager funcione
    if "sales" not in st.session_state:
        st.session_state.sales = []
        
    render_page()
