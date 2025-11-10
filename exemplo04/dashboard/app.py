# dashboard/app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import os
from datetime import datetime

# ===========================
# 🔧 CONFIGURAÇÕES INICIAIS
# ===========================
API_URL = os.environ.get("API_URL", "http://api:8000")
st.set_page_config(
    page_title="Dashboard das Vendas de Consoles",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ===========================
# 🎨 ESTILO VISUAL (cores e temas)
# ===========================
st.markdown("""
    <style>
    /* ===== Cards de Métricas ===== */
    div[data-testid="stMetric"] {
        background-color: #1A1C23     /* Fundo do card */
        border-radius: 20px;           /* Cantos arredondados */
        padding: 20px 15px;            /* Espaçamento interno */
        margin: 10px;                  /* Espaçamento entre os cards */
        box-shadow: 0 0 10px rgba(86, 172, 214, 0.8); /* Sombra verde */
        text-align: center;
        transition: 0.3s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(86, 172, 214, 0.8);
    }

    div[data-testid="stMetricLabel"] {
        color: #FFFFFF;                /* Cor do texto "Total de Vendas" */
        font-size: 1.1rem;
        font-weight: 500;
    }

    div[data-testid="stMetricValue"] {
        color: #48B9DB;                /* Cor do número */
        font-size: 1.8rem;             /* Tamanho maior do número */
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)
# 🎨 Cores personalizadas
st.title("📊 Análise de Vendas da GameWorld")
st.caption("Visualize, analise e insira dados de vendas em tempo real.")

# ===========================
# 📦 FUNÇÕES DE DADOS
# ===========================
@st.cache_data(ttl=300)
def carregar_vendas():
    response = requests.get(f"{API_URL}/vendas")
    response.raise_for_status()
    return pd.DataFrame(response.json())

@st.cache_data(ttl=300)
def carregar_analise():
    response = requests.get(f"{API_URL}/vendas/analise")
    response.raise_for_status()
    return pd.DataFrame(response.json())

def inserir_venda(dados):
    response = requests.post(f"{API_URL}/vendas", json=dados)
    return response.status_code in (200, 201)

# ===========================
# 🚀 APLICAÇÃO PRINCIPAL
# ===========================
try:
    df_vendas = carregar_vendas()
    df_analise = carregar_analise()

    # Caso a API retorne sem dados
    if df_vendas.empty:
        st.warning("Nenhuma venda registrada ainda. Adicione novas vendas na aba abaixo.")
    else:
        # ==================================
        # 📈 VISUALIZAÇÃO DE DADOS
        # ==================================
        tab1, tab2 = st.tabs(["📊 Análise de Vendas", "➕ Inserir Nova Venda"])

        with tab1:
            st.subheader("📌 Visão Geral")

            # =======================
            # KPIs (Indicadores)
            # =======================
            df_vendas["receita"] = df_vendas["valor"] * df_vendas["quantidade"]
            total_receita = df_vendas["receita"].sum()
            total_vendas = len(df_vendas)
            ticket_medio = total_receita / total_vendas if total_vendas > 0 else 0

            col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
            col_kpi1.metric("💰 Receita Total", f"R$ {total_receita:,.2f}")
            col_kpi2.metric("🛒 Total de Vendas", f"{total_vendas}")
            col_kpi3.metric("🏷️ Ticket Médio", f"R$ {ticket_medio:,.2f}")

            # =======================
            # FILTRO DE CATEGORIA
            # =======================
            categorias = ["Todas"] + sorted(df_vendas["categoria"].unique().tolist())
            categoria_selecionada = st.selectbox("🎯 Selecione uma categoria:", categorias)

            if categoria_selecionada != "Todas":
                df_filtrado = df_vendas[df_vendas["categoria"] == categoria_selecionada]
            else:
                df_filtrado = df_vendas.copy()

            # =======================
            # GRÁFICOS PRINCIPAIS
            # =======================
            col1, col2 = st.columns([2, 1])

            with col1:
                st.subheader("📦 Receita Total por Categoria")
                fig1 = px.bar(
                    df_analise,
                    x="categoria",
                    y="receita_total",
                    text_auto=True,
                    color="categoria",
                     color_discrete_sequence=["#10B9EC", "#0DCA8B", "#2C2C29", "#FF4444"], 
                    title="Receita Total por Categoria de Produto"
                )
                st.plotly_chart(fig1, use_container_width=True)

            with col2:
                st.subheader("🥧 Proporção de Vendas")
                fig2 = px.pie(
                    df_analise,
                    values="total_vendas",
                    names="categoria",
                    color_discrete_sequence=["#10B9EC", "#0DCA8B", "#2C2C29", "#FF4444"],
                    title="Distribuição de Vendas por Categoria"
                )
                st.plotly_chart(fig2, use_container_width=True)

            # =======================
            # GRÁFICO TEMPORAL
            # =======================
            st.subheader(f"📆 Evolução de Receita {' - ' + categoria_selecionada if categoria_selecionada != 'Todas' else ''}")
            df_filtrado["data_venda"] = pd.to_datetime(df_filtrado["data_venda"])
            df_por_data = df_filtrado.groupby("data_venda", as_index=False)["receita"].sum()

            fig3 = px.line(
                df_por_data,
                x="data_venda",
                y="receita",
                markers=True,
                color_discrete_sequence=["#10B9EC"],
                title="Evolução da Receita ao Longo do Tempo"
            )
            fig3.update_traces(line=dict(width=3))
            st.plotly_chart(fig3, use_container_width=True)

            # =======================
            # TABELA DE DADOS
            # =======================
            st.subheader("📋 Detalhes das Vendas")
            st.dataframe(df_filtrado, use_container_width=True, hide_index=True)

            # Botão de exportação
            st.download_button(
                "⬇️ Baixar Dados em CSV",
                data=df_filtrado.to_csv(index=False).encode("utf-8"),
                file_name="vendas.csv",
                mime="text/csv",
            )

        # ==================================
        # 🧾 FORMULÁRIO DE NOVAS VENDAS
        # ==================================
        with tab2:
            st.subheader("🧾 Adicionar Nova Venda")

            with st.form("nova_venda_form"):
                data_venda = st.date_input("Data da Venda", datetime.now().date())
                produto = st.text_input("Nome do Produto")

                usar_categoria_existente = st.checkbox("Usar categoria existente", value=True)
                if usar_categoria_existente and not df_vendas.empty:
                    categoria = st.selectbox("Categoria", sorted(df_vendas["categoria"].unique().tolist()))
                else:
                    categoria = st.text_input("Nova Categoria")

                valor = st.number_input("Valor Unitário (R$)", min_value=0.01, format="%.2f")
                quantidade = st.number_input("Quantidade", min_value=1, step=1)

                submitted = st.form_submit_button("💾 Adicionar Venda")

                if submitted:
                    if not produto.strip():
                        st.error("⚠️ O nome do produto não pode estar vazio.")
                    elif not categoria.strip():
                        st.error("⚠️ A categoria é obrigatória.")
                    elif valor <= 0:
                        st.error("⚠️ O valor deve ser maior que zero.")
                    elif quantidade < 1:
                        st.error("⚠️ A quantidade deve ser pelo menos 1.")
                    else:
                        nova_venda = {
                            "data_venda": data_venda.isoformat(),
                            "produto": produto,
                            "categoria": categoria,
                            "valor": valor,
                            "quantidade": quantidade
                        }
                        if inserir_venda(nova_venda):
                            st.success("✅ Venda adicionada com sucesso!")
                            # Limpa cache apenas dos datasets
                            carregar_vendas.clear()
                            carregar_analise.clear()
                            st.rerun()
                        else:
                            st.error("❌ Erro ao adicionar venda. Verifique os dados e tente novamente.")

except Exception as e:
    st.error(f"🚨 Erro ao carregar dados: {e}")
    st.warning("Verifique se a API está disponível e funcionando corretamente.")
