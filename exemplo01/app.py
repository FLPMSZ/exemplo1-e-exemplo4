import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ======================
# ⚙️ CONFIGURAÇÃO GERAL
# ======================
st.set_page_config(
    page_title="Vendas De Consoles em 2025",
    page_icon="🎮",
    layout="wide"
)

# ======================
# 🎨 ESTILO CUSTOMIZADO (Dark Theme)
# ======================
st.markdown("""
    <style>
    /* ======= Fundo geral ======= */
    .stApp {
        background-color: #000000;
        color: #5ED171;
        font-family: 'Segoe UI', sans-serif;
    }

    /* ======= Títulos ======= */
    h1, h2, h3 {
        color: #5ED171;
        font-weight: 700;
    }

    /* ======= Linha divisória ======= */
    hr {
        border: 1px solid #1f2937;
        margin: 1.5rem 0;
    }

    /* ======= Cards ======= */
    .card {
        background-color: #242B28;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 0 8px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }
    .card:hover {
        transform: translateY(-3px);
    }

    /* ======= Métricas ======= */
    div[data-testid="stMetricValue"] {
        color: #ffffff;
        font-weight: bold;
        font-size: 1.4rem;
    }

    /* ======= Sidebar ======= */
    section[data-testid="stSidebar"] {
        background-color: #1a1c23;
        color: white;
        border-right: 1px solid #2c2f36;
    }

    /* ======= Rodapé ======= */
    footer {
        visibility: hidden;
    }
    </style>
""", unsafe_allow_html=True)
# ======================
# 📊 DADOS DE EXEMPLO
# ======================
@st.cache_data
def load_data():
    data = {
        'Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
        'Vendas': [23000, 17100, 8500, 22300, 17645, 25000]
    }
    return pd.DataFrame(data)

df = load_data()

# ======================
# 🧾 CONTEÚDO PRINCIPAL
# ======================
st.title("🎮 Dashboard de Vendas dos Consoles da Games World no Primeiro Semestre de 2025")
st.markdown("---")

# ---- Cards de Métricas ----
total = df['Vendas'].sum()
media = df['Vendas'].mean()
crescimento = ((df['Vendas'].iloc[-1] / df['Vendas'].iloc[0]) - 1) * 100

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="card"><h3>💵 Total de Vendas</h3>', unsafe_allow_html=True)
    st.metric(label="", value=f"R$ {total:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card"><h3>📆 Média Mensal</h3>', unsafe_allow_html=True)
    st.metric(label="", value=f"R$ {media:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card"><h3>📈 Crescimento</h3>', unsafe_allow_html=True)
    st.metric(label="", value=f"{crescimento:.1f}%")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ---- Gráfico de Tendência ----
st.subheader("📊 Tendência de Vendas")
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df['Mês'], df['Vendas'], color="#030303", marker='o', linewidth=3)
ax.set_facecolor("#ffffff")
ax.grid(alpha=0.3, color="#03501c")
ax.set_ylabel('Vendas (R$)', fontsize=10, color="#000000")
ax.tick_params(colors="#000000")
for spine in ax.spines.values():
    spine.set_color("#135f1d")
st.pyplot(fig)

# ---- Tabela de dados ----
st.subheader("🧾 Tabela de Dados")
st.dataframe(df, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
