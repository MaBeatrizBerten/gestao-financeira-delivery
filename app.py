from datetime import date, datetime
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import database as db
import utils

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Dogueria Gestão Financeira",
    page_icon="🌭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Inicializa banco de dados e migrações
db.init_db()

# --- ESTILIZAÇÃO CSS CUSTOMIZADA (DARK GRAPHITE & FLAME ORANGE) ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', 'Inter', sans-serif;
    }

    /* Fundo da Aplicação */
    .stApp {
        background-color: #0F1015;
        color: #F3F4F6;
        max-width: 1200px;
        margin: 0 auto;
    }

    /* Cabeçalho Principal */
    .brand-header {
        text-align: center;
        padding: 10px 0 20px 0;
    }
    .brand-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #EDECEC;
        margin: 0;
    }
    .brand-subtitle {
        color: #9CA3AF;
        font-size: 1.5rem;
        font-weight: 500;
        margin-top: 4px;
    }

    /* Cards de Métricas Modernos */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #181A22 0%, #1E202B 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 16px 18px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: rgba(255, 112, 67, 0.4);
    }
    div[data-testid="stMetric"] label {
        color: #9CA3AF !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
    }

    /* Estilização das Abas (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #161822;
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }
    .stTabs [data-baseweb="tab"] {
        height: 42px;
        border-radius: 8px;
        color: #9CA3AF;
        font-weight: 600;
        font-size: 0.9rem;
        padding: 0 16px;
        border: none !important;
        background-color: transparent;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FF5E36 !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 12px rgba(255, 94, 54, 0.35);
    }

    /* Cards e Containers com estilo Glass/Dark */
    .custom-card {
        background: #181A22;
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }

    /* Inputs e Caixas de Formulário */
    div[data-baseweb="input"], div[data-baseweb="select"] > div {
        background-color: #13141B !important;
        border: 1px solid #2D313F !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
    }
    div[data-baseweb="input"]:focus-within, div[data-baseweb="select"] > div:focus-within {
        border-color: #FF7043 !important;
        box-shadow: 0 0 0 1px #FF7043 !important;
    }
    input, textarea {
        color: #FFFFFF !important;
    }

    /* Botões Primários */
    .stButton > button[kind="primary"], button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #FF5E36 0%, #FF7043 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 10px 22px !important;
        box-shadow: 0 4px 14px rgba(255, 94, 54, 0.35) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #E04B26 0%, #F4511E 100%) !important;
        transform: translateY(-1px);
    }

    /* Botões Secundários */
    .stButton > button[kind="secondary"], button[data-testid="baseButton-secondary"] {
        background-color: #202330 !important;
        color: #E5E7EB !important;
        border: 1px solid #32374A !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button[kind="secondary"]:hover {
        border-color: #FF7043 !important;
        color: #FF7043 !important;
        background-color: #272B3C !important;
    }

    /* Badges Customizados para Extrato */
    .badge-entrada {
        background-color: rgba(6, 214, 160, 0.15);
        color: #06D6A0;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.8rem;
        display: inline-block;
        border: 1px solid rgba(6, 214, 160, 0.3);
    }
    .badge-saida {
        background-color: rgba(239, 71, 111, 0.15);
        color: #EF476F;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.8rem;
        display: inline-block;
        border: 1px solid rgba(239, 71, 111, 0.3);
    }
    .badge-pago {
        background-color: rgba(17, 138, 178, 0.15);
        color: #38BDF8;
        padding: 2px 7px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.75rem;
        border: 1px solid rgba(56, 189, 248, 0.3);
    }
    .badge-pendente {
        background-color: rgba(255, 170, 0, 0.15);
        color: #FBBF24;
        padding: 2px 7px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.75rem;
        border: 1px solid rgba(251, 191, 36, 0.3);
    }
    .badge-pagamento {
        background-color: #242836;
        color: #D1D5DB;
        padding: 2px 7px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 500;
    }

    /* Linhas do Extrato */
    .extrato-row {
        background-color: #161822;
        border: 1px solid #232736;
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 8px;
        transition: background-color 0.15s ease;
    }
    .extrato-row:hover {
        background-color: #1D202D;
        border-color: #31364A;
    }

    hr {
        border-color: rgba(255, 255, 255, 0.08) !important;
        margin: 16px 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- CABEÇALHO DA APLICAÇÃO ---
st.markdown(
    """
    <div class="brand-header">
        <h1 class="brand-title"> DOGUERIA GESTÃO FINANCEIRA </h1>
        <div class="brand-subtitle">Sistema Integrado de Gestão Financeira, Vendas & Caixa Diário</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- LISTAS DE CATEGORIAS E OPÇÕES ---
CATEGORIAS_SAIDA = [
    "Insumos",
    "Embalagens e Descartáveis",
    "Motoboy / Taxas de Entrega",
    "Taxas / Comissões de Plataformas",
    "Gás / Energia / Água / Internet",
    "Equipamentos / Utensílios / Manutenção",
    "Marketing / Anúncios",
    "Pró-labore / Equipe",
    "Outros Gastos",
]

CATEGORIAS_ENTRADA = [
    "Vendas WhatsApp",
    "Vendas Presencial",
    "Vendas MenuDino",
    "Outras Receitas",
]

FORMAS_PAGAMENTO = [
    "Pix",
    "Cartão de Crédito",
    "Cartão de Débito",
    "Dinheiro",
]

STATUS_OPCOES = ["Pago", "Pendente"]


# --- DIÁLOGOS DE AÇÃO (MODAIS) ---
@st.dialog("✏️ Editar Lançamento")
def dialog_editar_registro(id_registro: int):
    reg = db.obter_registro_por_id(id_registro)
    if not reg:
        st.error("Registro não encontrado!")
        return

    data_val = (
        datetime.strptime(reg["data"], "%Y-%m-%d").date()
        if reg["data"]
        else date.today()
    )
    tipo_idx = 0 if reg["tipo"] == "Entrada" else 1

    with st.form("form_edicao"):
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            data_edit = st.date_input("Data", value=data_val, format="DD/MM/YYYY")
            tipo_edit = st.radio(
                "Tipo de Movimentação",
                ["Entrada", "Saída"],
                index=tipo_idx,
                horizontal=True,
            )

        with col_e2:
            opcoes_cat = (
                CATEGORIAS_ENTRADA if tipo_edit == "Entrada" else CATEGORIAS_SAIDA
            )
            cat_atual = (
                reg["categoria"] if reg["categoria"] in opcoes_cat else opcoes_cat[0]
            )
            categoria_edit = st.selectbox(
                "Categoria", opcoes_cat, index=opcoes_cat.index(cat_atual)
            )
            valor_edit = st.number_input(
                "Valor (R$)",
                min_value=0.01,
                value=float(reg["valor"]),
                step=5.0,
                format="%.2f",
            )

        col_e3, col_e4, col_e5 = st.columns([1.2, 1.2, 1])
        with col_e3:
            fp_atual = reg.get("forma_pagamento", "Pix")
            fp_idx = (
                FORMAS_PAGAMENTO.index(fp_atual) if fp_atual in FORMAS_PAGAMENTO else 0
            )
            forma_pag_edit = st.selectbox(
                "Forma de Pagamento", FORMAS_PAGAMENTO, index=fp_idx
            )

        with col_e4:
            st_atual = reg.get("status", "Pago")
            st_idx = STATUS_OPCOES.index(st_atual) if st_atual in STATUS_OPCOES else 0
            status_edit = st.selectbox("Status", STATUS_OPCOES, index=st_idx)

        with col_e5:
            qtd_atual = int(reg.get("qtd_pedidos", 1)) if reg.get("qtd_pedidos") else 1
            qtd_edit = st.number_input(
                "Qtd. Pedidos", min_value=1, value=qtd_atual, step=1
            )

        descricao_edit = st.text_input(
            "Observação / Descrição", value=reg.get("descricao", "")
        )

        st.markdown("<br>", unsafe_allow_html=True)
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            salvar = st.form_submit_button(
                "💾 Salvar Alterações", use_container_width=True, type="primary"
            )
        with col_b2:
            cancelar = st.form_submit_button("Cancelar", use_container_width=True)

        if salvar:
            db.atualizar_registro(
                id_registro,
                data_edit,
                tipo_edit,
                categoria_edit,
                descricao_edit,
                valor_edit,
                forma_pag_edit,
                status_edit,
                qtd_edit if tipo_edit == "Entrada" else 1,
            )
            st.success("✅ Registro atualizado com sucesso!")
            st.rerun()

        if cancelar:
            st.rerun()


@st.dialog("🗑️ Confirmar Exclusão")
def dialog_excluir_registro(id_registro: int):
    reg = db.obter_registro_por_id(id_registro)
    if not reg:
        st.error("Registro não encontrado!")
        return

    st.markdown(f"""
        Tem certeza que deseja apagar este lançamento?
        
        - **Data:** {reg['data']}
        - **Tipo:** {reg['tipo']}
        - **Categoria:** {reg['categoria']}
        - **Valor:** {utils.formatar_moeda(reg['valor'])}
        - **Descrição:** {reg.get('descricao') or '-'}
        """)
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        if st.button("🗑️ Sim, apagar", type="primary", use_container_width=True):
            db.deletar_registro(id_registro)
            st.toast("Lançamento apagado com sucesso!", icon="✅")
            st.rerun()
    with col_c2:
        if st.button("Cancelar", use_container_width=True):
            st.rerun()


# --- NAVEGAÇÃO POR ABAS ---
tab_dash, tab_novo, tab_extrato, tab_caixa, tab_config = st.tabs(
    [
        "📊 Dashboard & Métricas",
        "➕ Novo Lançamento",
        "📋 Extrato & Gestão",
        "🛵 Fechamento de Caixa",
        "⚙️ Backup & Ajustes",
    ]
)

# Carrega dados atualizados
df_geral = db.carregar_dados()

# ==============================================================================
# ABA 1: DASHBOARD & MÉTRICAS
# ==============================================================================
with tab_dash:
    if df_geral.empty:
        st.info(
            "👋 Bem-vindo! Nenhum lançamento encontrado. Vá até a aba **'➕ Novo Lançamento'** para registrar suas vendas e gastos."
        )
    else:
        # Filtros de Período
        col_f1, col_f2, col_f3 = st.columns([1.5, 1.5, 2])
        anos_disponiveis = sorted(df_geral["ano"].dropna().unique(), reverse=True)
        ano_selecionado = col_f1.selectbox("📅 Ano", anos_disponiveis, key="dash_ano")

        df_ano = df_geral[df_geral["ano"] == ano_selecionado]
        meses_opcoes = ["Todos os Meses"] + sorted(
            df_ano["mes_ano"].dropna().unique().tolist(), reverse=True
        )
        mes_selecionado = col_f2.selectbox("🗓️ Mês", meses_opcoes, key="dash_mes")

        apenas_pagos = col_f3.checkbox(
            "Considerar apenas valores já pagos/recebidos", value=False
        )

        # Filtragem do DataFrame
        df_dash = df_ano.copy()
        if mes_selecionado != "Todos os Meses":
            df_dash = df_dash[df_dash["mes_ano"] == mes_selecionado]

        if apenas_pagos:
            df_dash = df_dash[df_dash["status"] == "Pago"]

        # Cálculos de Métricas
        entradas_df = df_dash[df_dash["tipo"] == "Entrada"]
        saidas_df = df_dash[df_dash["tipo"] == "Saída"]

        total_entradas = entradas_df["valor"].sum()
        total_saidas = saidas_df["valor"].sum()
        lucro_liquido = total_entradas - total_saidas
        margem_lucro = (
            (lucro_liquido / total_entradas * 100) if total_entradas > 0 else 0.0
        )

        total_pedidos = entradas_df["qtd_pedidos"].sum() if not entradas_df.empty else 0
        ticket_medio = (total_entradas / total_pedidos) if total_pedidos > 0 else 0.0

        # Pendências (Contas a pagar / receber no período)
        pend_pagar = saidas_df[saidas_df["status"] == "Pendente"]["valor"].sum()
        pend_receber = entradas_df[entradas_df["status"] == "Pendente"]["valor"].sum()

        # Grid de KPIs
        st.markdown("<br>", unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("🟢 Faturamento Total", utils.formatar_moeda(total_entradas))
        m2.metric("🔴 Gastos Totais", utils.formatar_moeda(total_saidas))
        m3.metric("💰 Lucro Líquido", utils.formatar_moeda(lucro_liquido))
        m4.metric("📈 Margem Líquida", utils.formatar_percentual(margem_lucro))

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("🌭 Total de Pedidos", f"{int(total_pedidos)}")
        k2.metric("🏷️ Ticket Médio", utils.formatar_moeda(ticket_medio))
        k3.metric("⏳ A Pagar (Pendente)", utils.formatar_moeda(pend_pagar))
        k4.metric("⏳ A Receber (Pendente)", utils.formatar_moeda(pend_receber))

        st.markdown("---")

        # Gráficos
        g_col1, g_col2 = st.columns(2)

        with g_col1:
            st.markdown("### 📈 Evolução Financeira")
            if mes_selecionado != "Todos os Meses":
                # Agrupado por Dia
                df_evol = (
                    df_dash.groupby(["dia_mes", "tipo"])["valor"].sum().reset_index()
                )
                if not df_evol.empty:
                    fig_evol = px.bar(
                        df_evol,
                        x="dia_mes",
                        y="valor",
                        color="tipo",
                        barmode="group",
                        labels={"dia_mes": "Dia", "valor": "R$", "tipo": "Tipo"},
                        color_discrete_map={"Entrada": "#06D6A0", "Saída": "#EF476F"},
                    )
                else:
                    fig_evol = None
            else:
                # Agrupado por Mês
                df_evol = (
                    df_dash.groupby(["mes_ano", "tipo"])["valor"].sum().reset_index()
                )
                if not df_evol.empty:
                    fig_evol = px.bar(
                        df_evol,
                        x="mes_ano",
                        y="valor",
                        color="tipo",
                        barmode="group",
                        labels={"mes_ano": "Mês", "valor": "R$", "tipo": "Tipo"},
                        color_discrete_map={"Entrada": "#06D6A0", "Saída": "#EF476F"},
                    )
                else:
                    fig_evol = None

            if fig_evol:
                fig_evol.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#D1D5DB", family="Poppins"),
                    margin=dict(t=20, b=20, l=10, r=10),
                    legend=dict(
                        orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
                    ),
                    xaxis=dict(showgrid=False, color="#9CA3AF"),
                    yaxis=dict(gridcolor="rgba(255,255,255,0.06)", color="#9CA3AF"),
                )
                st.plotly_chart(fig_evol, use_container_width=True)
            else:
                st.info("Sem dados suficientes para o gráfico de evolução.")

        with g_col2:
            st.markdown("### 🍩 Gastos por Categoria")
            if not saidas_df.empty:
                df_cat_gastos = (
                    saidas_df.groupby("categoria")["valor"].sum().reset_index()
                )
                fig_gastos = px.pie(
                    df_cat_gastos,
                    values="valor",
                    names="categoria",
                    hole=0.45,
                    color_discrete_sequence=[
                        "#FF5E36",
                        "#FFAA00",
                        "#FFD166",
                        "#EF476F",
                        "#118AB2",
                        "#06D6A0",
                        "#8338EC",
                    ],
                )
                fig_gastos.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#D1D5DB", family="Poppins"),
                    margin=dict(t=20, b=20, l=10, r=10),
                    legend=dict(orientation="v", font=dict(size=11)),
                )
                st.plotly_chart(fig_gastos, use_container_width=True)
            else:
                st.info("Nenhum gasto registrado neste período.")

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        c_col1, c_col2 = st.columns(2)

        with c_col1:
            st.markdown("### 🛵 Vendas por Canal")
            if not entradas_df.empty:
                df_canais = (
                    entradas_df.groupby("categoria")["valor"].sum().reset_index()
                )
                fig_canais = px.pie(
                    df_canais,
                    values="valor",
                    names="categoria",
                    hole=0.45,
                    color_discrete_sequence=[
                        "#06D6A0",
                        "#118AB2",
                        "#FFD166",
                        "#FFAA00",
                        "#FF5E36",
                    ],
                )
                fig_canais.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#D1D5DB", family="Poppins"),
                    margin=dict(t=20, b=20, l=10, r=10),
                )
                st.plotly_chart(fig_canais, use_container_width=True)
            else:
                st.info("Nenhuma venda registrada no período.")

        with c_col2:
            st.markdown("### 💳 Meios de Pagamento")
            if not entradas_df.empty:
                df_pagamentos = (
                    entradas_df.groupby("forma_pagamento")["valor"].sum().reset_index()
                )
                fig_pag = px.bar(
                    df_pagamentos,
                    x="forma_pagamento",
                    y="valor",
                    color="forma_pagamento",
                    labels={"forma_pagamento": "Forma de Pagamento", "valor": "R$"},
                    color_discrete_sequence=[
                        "#118AB2",
                        "#06D6A0",
                        "#FFD166",
                        "#FF5E36",
                        "#8338EC",
                    ],
                )
                fig_pag.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#D1D5DB", family="Poppins"),
                    showlegend=False,
                    margin=dict(t=20, b=20, l=10, r=10),
                    xaxis=dict(showgrid=False, color="#9CA3AF"),
                    yaxis=dict(gridcolor="rgba(255,255,255,0.06)", color="#9CA3AF"),
                )
                st.plotly_chart(fig_pag, use_container_width=True)
            else:
                st.info("Sem lançamentos de pagamentos.")

# ==============================================================================
# ABA 2: NOVO LANÇAMENTO
# ==============================================================================
with tab_novo:
    st.markdown("### 📝 Registrar Nova Movimentação Financeira")
    st.caption(
        "Cadastre vendas diárias ou despesas operacionais da dogueria com rapidez."
    )

    with st.form("form_novo_lancamento", clear_on_submit=True):
        f_col1, f_col2 = st.columns(2)

        with f_col1:
            data_lanc = st.date_input(
                "Data da Movimentação", value=date.today(), format="DD/MM/YYYY"
            )
            tipo_lanc = st.radio(
                "Tipo",
                ["🔴 Saída (Gasto / Despesa)", "🟢 Entrada (Venda / Receita)"],
                horizontal=True,
            )

        is_entrada = "Entrada" in tipo_lanc

        with f_col2:
            if is_entrada:
                cat_opcoes = CATEGORIAS_ENTRADA
            else:
                cat_opcoes = CATEGORIAS_SAIDA

            categoria_lanc = st.selectbox("Categoria", cat_opcoes)
            valor_lanc = st.number_input(
                "Valor Total (R$)", min_value=0.01, step=5.0, format="%.2f"
            )

        st.markdown("---")
        f_col3, f_col4, f_col5 = st.columns([1.2, 1.2, 1])

        with f_col3:
            forma_pag_lanc = st.selectbox("Forma de Pagamento", FORMAS_PAGAMENTO)

        with f_col4:
            status_lanc = st.selectbox(
                "Status",
                ["Pago", "Pendente"],
                help="Selecione 'Pendente' para despesas agendadas a pagar ou vendas a compensar.",
            )

        with f_col5:
            if is_entrada:
                qtd_pedidos_lanc = st.number_input(
                    "Qtd. de Pedidos",
                    min_value=1,
                    value=1,
                    step=1,
                    help="Para cálculo automático do ticket médio.",
                )
            else:
                qtd_pedidos_lanc = 1
                st.caption("Fixo em 1 para despesas")

        descricao_lanc = st.text_input(
            "Observação / Descrição detalhada (opcional)",
            placeholder="Ex: 5kg de salsicha perdigão, 50 pães sovados, motoboy João...",
        )

        st.markdown("<br>", unsafe_allow_html=True)
        salvar_btn = st.form_submit_button(
            "💾 Salvar Lançamento", type="primary", use_container_width=True
        )

        if salvar_btn:
            tipo_salvar = "Entrada" if is_entrada else "Saída"
            db.salvar_registro(
                data=data_lanc,
                tipo=tipo_salvar,
                categoria=categoria_lanc,
                descricao=descricao_lanc,
                valor=valor_lanc,
                forma_pagamento=forma_pag_lanc,
                status=status_lanc,
                qtd_pedidos=qtd_pedidos_lanc,
            )
            st.toast("✅ Lançamento registrado com sucesso!", icon="🎉")
            st.rerun()

# ==============================================================================
# ABA 3: EXTRATO & GESTÃO
# ==============================================================================
with tab_extrato:
    st.markdown("### 📋 Extrato de Lançamentos & Gestão")
    st.caption("Filtre, pesquise, edite (✏️) ou exclua (🗑️) registros com segurança.")

    if df_geral.empty:
        st.info("Nenhum lançamento cadastrado no sistema.")
    else:
        # Filtros Dinâmicos
        filt_c1, filt_c2, filt_c3, filt_c4, filt_c5 = st.columns(
            [1.8, 1.2, 1.5, 1.2, 1.2]
        )

        with filt_c1:
            busca_texto = st.text_input(
                "🔍 Buscar por texto/obs", placeholder="Digite algo..."
            )

        with filt_c2:
            filtro_tipo = st.selectbox("Tipo", ["Todos", "Entradas", "Saídas"])

        with filt_c3:
            todas_cats = ["Todas"] + sorted(
                df_geral["categoria"].dropna().unique().tolist()
            )
            filtro_cat = st.selectbox("Categoria", todas_cats)

        with filt_c4:
            filtro_forma = st.selectbox("Pagamento", ["Todos"] + FORMAS_PAGAMENTO)

        with filt_c5:
            filtro_status = st.selectbox("Status", ["Todos", "Pago", "Pendente"])

        # Aplicação dos Filtros
        df_filtrado = df_geral.copy()

        if busca_texto:
            df_filtrado = df_filtrado[
                df_filtrado["descricao"].str.contains(busca_texto, case=False, na=False)
                | df_filtrado["categoria"].str.contains(
                    busca_texto, case=False, na=False
                )
            ]

        if filtro_tipo == "Entradas":
            df_filtrado = df_filtrado[df_filtrado["tipo"] == "Entrada"]
        elif filtro_tipo == "Saídas":
            df_filtrado = df_filtrado[df_filtrado["tipo"] == "Saída"]

        if filtro_cat != "Todas":
            df_filtrado = df_filtrado[df_filtrado["categoria"] == filtro_cat]

        if filtro_forma != "Todos":
            df_filtrado = df_filtrado[df_filtrado["forma_pagamento"] == filtro_forma]

        if filtro_status != "Todos":
            df_filtrado = df_filtrado[df_filtrado["status"] == filtro_status]

        # Botões de Exportação
        exp_col1, exp_col2, exp_col3 = st.columns([2, 1, 1])
        with exp_col1:
            st.markdown(f"**Exibindo {len(df_filtrado)} de {len(df_geral)} registros**")

        with exp_col2:
            excel_bytes = utils.gerar_excel(df_filtrado)
            st.download_button(
                label="📥 Baixar Excel (.xlsx)",
                data=excel_bytes,
                file_name=f"extrato_dogueria_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

        with exp_col3:
            csv_bytes = utils.gerar_csv(df_filtrado)
            st.download_button(
                label="📄 Baixar CSV",
                data=csv_bytes,
                file_name=f"extrato_dogueria_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True,
            )

        st.markdown("<hr style='margin: 8px 0;'>", unsafe_allow_html=True)

        # Cabeçalho da Tabela
        h_cols = st.columns([1.1, 1.1, 2.2, 1.3, 1.0, 1.4, 0.5, 0.5])
        h_cols[0].markdown("**Data**")
        h_cols[1].markdown("**Tipo**")
        h_cols[2].markdown("**Categoria & Descrição**")
        h_cols[3].markdown("**Pagamento**")
        h_cols[4].markdown("**Status**")
        h_cols[5].markdown("**Valor**")
        h_cols[6].markdown("**Editar**")
        h_cols[7].markdown("**Apagar**")

        st.markdown("<hr style='margin: 4px 0 10px 0;'>", unsafe_allow_html=True)

        if df_filtrado.empty:
            st.info("Nenhum lançamento corresponde aos filtros selecionados.")
        else:
            for _, row in df_filtrado.iterrows():
                r_cols = st.columns([1.1, 1.1, 2.2, 1.3, 1.0, 1.4, 0.5, 0.5])

                # Data
                dt_str = (
                    row["data"].strftime("%d/%m/%Y") if pd.notna(row["data"]) else "-"
                )
                r_cols[0].write(f"`{dt_str}`")

                # Tipo com Badge
                if row["tipo"] == "Entrada":
                    r_cols[1].markdown(
                        "<span class='badge-entrada'>🟢 Entrada</span>",
                        unsafe_allow_html=True,
                    )
                else:
                    r_cols[1].markdown(
                        "<span class='badge-saida'>🔴 Saída</span>",
                        unsafe_allow_html=True,
                    )

                # Categoria & Descrição
                desc = (
                    f" <small style='color: #9CA3AF;'>({row['descricao']})</small>"
                    if row["descricao"]
                    else ""
                )
                r_cols[2].markdown(
                    f"**{row['categoria']}**{desc}", unsafe_allow_html=True
                )

                # Forma de Pagamento
                fp_nome = row.get("forma_pagamento") or "Pix"
                r_cols[3].markdown(
                    f"<span class='badge-pagamento'>{fp_nome}</span>",
                    unsafe_allow_html=True,
                )

                # Status
                st_nome = row.get("status") or "Pago"
                if st_nome == "Pago":
                    r_cols[4].markdown(
                        "<span class='badge-pago'>✅ Pago</span>",
                        unsafe_allow_html=True,
                    )
                else:
                    r_cols[4].markdown(
                        "<span class='badge-pendente'>⏳ Pendente</span>",
                        unsafe_allow_html=True,
                    )

                # Valor
                val_fmt = utils.formatar_moeda(row["valor"])
                if row["tipo"] == "Entrada":
                    r_cols[5].markdown(
                        f"<span style='color: #06D6A0; font-weight: 700;'>{val_fmt}</span>",
                        unsafe_allow_html=True,
                    )
                else:
                    r_cols[5].markdown(
                        f"<span style='color: #EF476F; font-weight: 700;'>{val_fmt}</span>",
                        unsafe_allow_html=True,
                    )

                # Botão Editar
                if r_cols[6].button(
                    "✏️", key=f"btn_edit_{row['id']}", help="Editar este lançamento"
                ):
                    dialog_editar_registro(row["id"])

                # Botão Excluir
                if r_cols[7].button(
                    "🗑️", key=f"btn_del_{row['id']}", help="Apagar este lançamento"
                ):
                    dialog_excluir_registro(row["id"])

# ==============================================================================
# ABA 4: FECHAMENTO DE CAIXA DIÁRIO
# ==============================================================================
with tab_caixa:
    st.markdown("### 🛵 Fechamento de Caixa do Turno")
    st.caption(
        "Confira as vendas do dia, fundo de troco, sangrias e gaveta de dinheiro."
    )

    col_dt, _ = st.columns([2, 3])
    with col_dt:
        data_caixa = st.date_input(
            "Selecione o Dia do Turno", value=date.today(), format="DD/MM/YYYY"
        )

    data_caixa_str = data_caixa.strftime("%Y-%m-%d")
    resumo_dia = db.obter_resumo_dia(data_caixa_str)

    # Cards de Resumo do Sistema
    st.markdown("#### 📊 Movimentação Registrada no Sistema neste Dia")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(
        "💵 Vendas em Dinheiro", utils.formatar_moeda(resumo_dia["vendas_dinheiro"])
    )
    c2.metric("📱 Vendas em Pix", utils.formatar_moeda(resumo_dia["vendas_pix"]))
    c3.metric("💳 Vendas em Cartão", utils.formatar_moeda(resumo_dia["vendas_cartao"]))
    c4.metric(
        "🛵 Vendas no iFood / Plataformas",
        utils.formatar_moeda(resumo_dia["vendas_ifood"]),
    )

    st.markdown("<br>", unsafe_allow_html=True)

    with st.form("form_fechamento_caixa"):
        st.markdown("#### 🔒 Conferência da Gaveta de Dinheiro Físico")
        fc1, fc2, fc3 = st.columns(3)

        with fc1:
            fundo_troco = st.number_input(
                "Fundo de Troco Inicial (R$)",
                min_value=0.0,
                value=50.0,
                step=10.0,
                format="%.2f",
                help="Dinheiro que já estava na gaveta na abertura do caixa.",
            )

        with fc2:
            sangrias = st.number_input(
                "Sangrias / Retiradas de Dinheiro no Turno (R$)",
                min_value=0.0,
                value=0.0,
                step=10.0,
                format="%.2f",
                help="Dinheiro retirado da gaveta durante o turno.",
            )

        with fc3:
            dinheiro_gaveta = st.number_input(
                "Dinheiro Físico Contado na Gaveta no Fechamento (R$)",
                min_value=0.0,
                value=0.0,
                step=10.0,
                format="%.2f",
                help="Valor real de notas e moedas contados no fechamento.",
            )

        obs_caixa = st.text_input(
            "Observações do Turno (Opcional)",
            placeholder="Ex: Faltou troco no início, sangria para compra de pão...",
        )

        # Cálculos de Conferência
        vendas_dinheiro = resumo_dia["vendas_dinheiro"]
        saidas_dinheiro = resumo_dia["saidas_dinheiro"]

        dinheiro_esperado = fundo_troco + vendas_dinheiro - saidas_dinheiro - sangrias
        diferenca = dinheiro_gaveta - dinheiro_esperado

        st.markdown("---")
        res1, res2, res3 = st.columns(3)
        res1.markdown(
            f"**Total Vendas Dinheiro:** {utils.formatar_moeda(vendas_dinheiro)}"
        )
        res2.markdown(
            f"**Dinheiro Esperado na Gaveta:** `{utils.formatar_moeda(dinheiro_esperado)}`"
        )

        if diferenca == 0:
            res3.markdown(
                f"<span style='color: #06D6A0; font-weight: 700;'>Diferença: {utils.formatar_moeda(diferenca)} (Caixa Batendo!)</span>",
                unsafe_allow_html=True,
            )
        elif diferenca > 0:
            res3.markdown(
                f"<span style='color: #FFAA00; font-weight: 700;'>Diferença: +{utils.formatar_moeda(diferenca)} (Sobra no Caixa)</span>",
                unsafe_allow_html=True,
            )
        else:
            res3.markdown(
                f"<span style='color: #EF476F; font-weight: 700;'>Diferença: {utils.formatar_moeda(diferenca)} (Falta no Caixa)</span>",
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)
        gravar_caixa = st.form_submit_button(
            "🔒 Salvar Fechamento de Caixa", type="primary", use_container_width=True
        )

        if gravar_caixa:
            db.salvar_fechamento_caixa(
                data_str=data_caixa_str,
                fundo_troco=fundo_troco,
                dinheiro_gaveta=dinheiro_gaveta,
                total_dinheiro=vendas_dinheiro,
                total_pix=resumo_dia["vendas_pix"],
                total_cartao=resumo_dia["vendas_cartao"],
                total_ifood=resumo_dia["vendas_ifood"],
                total_saidas_dinheiro=saidas_dinheiro,
                sangria=sangrias,
                diferenca=diferenca,
                observacao=obs_caixa,
            )
            st.toast("✅ Fechamento de caixa gravado com sucesso!", icon="🔒")
            st.rerun()

    # Histórico de Fechamentos
    st.markdown("---")
    st.markdown("#### 📜 Histórico de Fechamentos Salvos")
    df_fech = db.carregar_fechamentos_caixa()

    if df_fech.empty:
        st.info("Nenhum fechamento de caixa arquivado ainda.")
    else:
        for _, frow in df_fech.iterrows():
            with st.expander(
                f"📅 Fechamento de {frow['data']} | Gaveta: {utils.formatar_moeda(frow['dinheiro_gaveta'])} (Dif: {utils.formatar_moeda(frow['diferenca'])})"
            ):
                c_a, c_b, c_c, c_d = st.columns(4)
                c_a.write(
                    f"**Fundo Inicial:** {utils.formatar_moeda(frow['fundo_troco'])}"
                )
                c_b.write(
                    f"**Vendas Dinheiro:** {utils.formatar_moeda(frow['total_dinheiro'])}"
                )
                c_c.write(f"**Sangrias:** {utils.formatar_moeda(frow['sangria'])}")
                c_d.write(
                    f"**Vendas Pix/Cartão:** {utils.formatar_moeda(frow['total_pix'] + frow['total_cartao'])}"
                )
                if frow["observacao"]:
                    st.write(f"**Obs:** {frow['observacao']}")

# ==============================================================================
# ABA 5: BACKUP & AJUSTES
# ==============================================================================
with tab_config:
    st.markdown("### ⚙️ Backup & Segurança dos Dados")
    st.caption("Faça download periódico da cópia de segurança do seu banco de dados.")

    cfg1, cfg2 = st.columns(2)

    with cfg1:
        st.markdown("#### 💾 Download de Backup")
        st.write(
            "Baixe uma cópia exata do arquivo `financeiro_delivery.db` contendo todas as vendas, despesas e caixas."
        )
        backup_bytes = utils.obter_backup_db()
        st.download_button(
            label="📦 Baixar Backup do Banco de Dados (.db)",
            data=backup_bytes,
            file_name=f"backup_financeiro_delivery_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db",
            mime="application/x-sqlite3",
            type="primary",
            use_container_width=True,
        )

    with cfg2:
        st.markdown("#### 🔄 Restaurar Backup")
        st.write("Suba um arquivo `.db` salvo anteriormente para restaurar o sistema.")
        uploaded_db = st.file_uploader(
            "Selecione o arquivo .db de backup", type=["db", "sqlite", "sqlite3"]
        )

        if uploaded_db is not None:
            if st.button(
                "⚠️ Confirmar Restauração do Banco",
                type="secondary",
                use_container_width=True,
            ):
                sucesso = utils.restaurar_backup_db(uploaded_db.getvalue())
                if sucesso:
                    st.success("✅ Banco de dados restaurado com sucesso!")
                    st.rerun()
                else:
                    st.error("Erro ao restaurar o banco de dados.")

    st.markdown("---")
    st.markdown("#### ℹ️ Informações do Sistema")
    st.markdown(f"""
        - **Total de lançamentos cadastrados:** {len(df_geral)}
        - **Banco de Dados:** SQLite 3 (`financeiro_delivery.db`)
        - **Versão:** 2.0 (Modernizada para Delivery & Dogueria)
        """)
