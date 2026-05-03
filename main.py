import streamlit as st
import numpy as np
from scipy.integrate import odeint
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ──────────────────────────────────────────────
# Configuração da página
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Simulador SEIR",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# CSS personalizado
# ──────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', sans-serif;
    }

    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #21262d;
    }
    [data-testid="stSidebar"] * {
        color: #c9d1d9 !important;
    }

    /* Título principal */
    .titulo-principal {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 2.2rem;
        font-weight: 600;
        color: #58a6ff;
        letter-spacing: -1px;
        margin-bottom: 0;
        line-height: 1.1;
    }
    .subtitulo {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.85rem;
        color: #8b949e;
        margin-top: 4px;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .divider {
        border: none;
        border-top: 1px solid #21262d;
        margin: 18px 0;
    }

    /* Cards de métricas */
    .metric-card {
        background: #161b22;
        border: 1px solid #21262d;
        border-radius: 8px;
        padding: 18px 22px;
        text-align: center;
        transition: border-color 0.2s;
    }
    .metric-card:hover { border-color: #58a6ff44; }
    .metric-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #8b949e;
        margin-bottom: 6px;
    }
    .metric-value {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1.7rem;
        font-weight: 600;
    }
    .metric-sub {
        font-size: 0.75rem;
        color: #8b949e;
        margin-top: 3px;
    }

    /* R0 badge */
    .r0-badge {
        display: inline-block;
        background: #0d419d22;
        border: 1px solid #1f6feb;
        border-radius: 20px;
        padding: 6px 20px;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1rem;
        color: #58a6ff;
        margin: 0 auto;
    }

    /* Sidebar section label */
    .sidebar-section {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #8b949e;
        margin-top: 16px;
        margin-bottom: 4px;
    }

    /* Esconder menu do Streamlit */
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Modelo SEIR — EDOs
# ──────────────────────────────────────────────
def modelo_seir(y, t, N, beta, sigma, gamma):
    """
    Define as Equações Diferenciais Ordinárias do modelo SEIR.
    
    Parâmetros:
        y     : vetor de estado [S, E, I, R]
        t     : tempo
        N     : população total
        beta  : taxa de transmissão
        sigma : taxa de progressão (1 / período de incubação)
        gamma : taxa de recuperação (1 / período de infecção)
    """
    S, E, I, R = y
    dS = -beta * S * I / N
    dE =  beta * S * I / N - sigma * E
    dI =  sigma * E - gamma * I
    dR =  gamma * I
    return dS, dE, dI, dR


def executar_simulacao(N, beta, sigma, gamma, dias, E0=1, I0=0):
    """Resolve o sistema de EDOs e retorna os resultados."""
    S0 = N - E0 - I0
    R0_inicial = 0
    y0 = S0, E0, I0, R0_inicial
    t = np.linspace(0, dias, dias * 4)  # 4 pontos por dia para suavidade
    resultado = odeint(modelo_seir, y0, t, args=(N, beta, sigma, gamma))
    S, E, I, R = resultado.T
    return t, S, E, I, R


# ──────────────────────────────────────────────
# Sidebar — Controles
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="titulo-principal" style="font-size:1.3rem;">⚙️ Parâmetros</p>', unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown('<p class="sidebar-section">🌍 População</p>', unsafe_allow_html=True)
    N = st.slider(
        "População Inicial (N)",
        min_value=10_000, max_value=10_000_000,
        value=1_000_000, step=10_000,
        format="%d",
        help="Tamanho total da população simulada."
    )

    st.markdown('<p class="sidebar-section">🦠 Transmissão</p>', unsafe_allow_html=True)
    beta = st.slider(
        "Taxa de Transmissão (β)",
        min_value=0.05, max_value=1.50,
        value=0.30, step=0.01,
        help="Número médio de contatos infecciosos por dia."
    )

    st.markdown('<p class="sidebar-section">⏳ Períodos Clínicos</p>', unsafe_allow_html=True)
    periodo_incubacao = st.slider(
        "Período de Incubação (dias)",
        min_value=1, max_value=21,
        value=5, step=1,
        help="Tempo médio entre a exposição e o início da infecciosidade."
    )
    periodo_infeccao = st.slider(
        "Período de Infecção (dias)",
        min_value=1, max_value=30,
        value=10, step=1,
        help="Tempo médio que um indivíduo permanece infeccioso."
    )

    st.markdown('<p class="sidebar-section">📅 Horizonte</p>', unsafe_allow_html=True)
    dias = st.slider(
        "Tempo de Simulação (dias)",
        min_value=30, max_value=730,
        value=180, step=10,
        help="Duração total da simulação em dias."
    )

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown(
        '<p style="font-size:0.72rem; color:#8b949e; font-family:\'IBM Plex Mono\',monospace;">'
        'Modelo SEIR · Scipy odeint<br>Visualização Plotly · Interface Streamlit'
        '</p>',
        unsafe_allow_html=True
    )


# ──────────────────────────────────────────────
# Cálculos derivados
# ──────────────────────────────────────────────
sigma = 1.0 / periodo_incubacao
gamma = 1.0 / periodo_infeccao
R0    = beta / gamma  # Número básico de reprodução

t, S, E, I, R_vals = executar_simulacao(N, beta, sigma, gamma, dias)

pico_infeccao      = int(I.max())
dia_pico           = int(t[np.argmax(I)])
total_infectados   = int(R_vals[-1])
suscetivel_final   = int(S[-1])
percentual_afetado = (total_infectados / N) * 100


# ──────────────────────────────────────────────
# Cabeçalho
# ──────────────────────────────────────────────
col_titulo, col_r0 = st.columns([3, 1])
with col_titulo:
    st.markdown('<p class="titulo-principal">🦠 Simulador Epidemiológico SEIR</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitulo">Suscetível · Exposto · Infectado · Recuperado</p>', unsafe_allow_html=True)
with col_r0:
    cor_r0 = "#3fb950" if R0 < 1 else ("#d29922" if R0 < 2 else "#f85149")
    status_r0 = "Controlada" if R0 < 1 else ("Limítrofe" if R0 < 2 else "Epidêmica")
    st.markdown(f"""
    <div style="text-align:right; padding-top:8px;">
        <div class="metric-label">Número de Reprodução Básico</div>
        <div style="font-family:'IBM Plex Mono',monospace; font-size:2.4rem; font-weight:600; color:{cor_r0}; line-height:1.1;">
            R₀ = {R0:.2f}
        </div>
        <div style="font-size:0.78rem; color:{cor_r0}; margin-top:2px;">● {status_r0}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Cards de métricas
# ──────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)

metricas = [
    (c1, "🏥 Pico de Infectados",  f"{pico_infeccao:,}",     f"Dia {dia_pico}",      "#f85149"),
    (c2, "📅 Dia do Pico",         f"Dia {dia_pico}",        f"β={beta:.2f}, γ={gamma:.3f}", "#d29922"),
    (c3, "👥 Total Afetados",      f"{total_infectados:,}",  f"{percentual_afetado:.1f}% da pop.", "#3fb950"),
    (c4, "🛡️ Nunca Infectados",   f"{suscetivel_final:,}",  f"{(suscetivel_final/N*100):.1f}% da pop.", "#58a6ff"),
]

for col, label, valor, sub, cor in metricas:
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value" style="color:{cor};">{valor}</div>
            <div class="metric-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Gráfico principal — Curvas SEIR
# ──────────────────────────────────────────────
CORES = {
    "S": "#58a6ff",   # Azul — Suscetível
    "E": "#d29922",   # Amarelo — Exposto
    "I": "#f85149",   # Vermelho — Infectado
    "R": "#3fb950",   # Verde — Recuperado
}

fig = go.Figure()

traces = [
    ("S", S,      "Suscetível (S)", "dash"),
    ("E", E,      "Exposto (E)",    "dot"),
    ("I", I,      "Infectado (I)",  "solid"),
    ("R", R_vals, "Recuperado (R)", "longdash"),
]

for key, dados, nome, dash in traces:
    fig.add_trace(go.Scatter(
        x=t, y=dados,
        name=nome,
        line=dict(color=CORES[key], width=2.5, dash=dash),
        hovertemplate=f"<b>{nome}</b><br>Dia: %{{x:.0f}}<br>Pessoas: %{{y:,.0f}}<extra></extra>",
        fill="tozeroy" if key == "I" else "none",
        fillcolor="rgba(248,81,73,0.06)" if key == "I" else None,
    ))

# Linha vertical no pico
fig.add_vline(
    x=dia_pico, line_dash="dash",
    line_color="#8b949e", line_width=1,
    annotation_text=f" Pico: Dia {dia_pico}",
    annotation_font_color="#8b949e",
    annotation_font_size=11,
)

fig.update_layout(
    title=dict(
        text="Dinâmica Epidemiológica — Modelo SEIR",
        font=dict(family="IBM Plex Mono", size=15, color="#c9d1d9"),
        x=0,
    ),
    plot_bgcolor="#0d1117",
    paper_bgcolor="#0d1117",
    font=dict(family="IBM Plex Sans", color="#8b949e"),
    xaxis=dict(
        title="Dias", gridcolor="#21262d", zerolinecolor="#21262d",
        tickfont=dict(family="IBM Plex Mono"),
    ),
    yaxis=dict(
        title="Número de Indivíduos", gridcolor="#21262d", zerolinecolor="#21262d",
        tickformat=",",
        tickfont=dict(family="IBM Plex Mono"),
    ),
    legend=dict(
        bgcolor="#161b22", bordercolor="#21262d", borderwidth=1,
        font=dict(family="IBM Plex Mono", size=12),
        orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
    ),
    hovermode="x unified",
    margin=dict(l=60, r=30, t=60, b=50),
    height=480,
)

st.plotly_chart(fig, use_container_width=True)


# ──────────────────────────────────────────────
# Gráfico secundário — Novos casos diários
# ──────────────────────────────────────────────
novos_casos = np.diff(R_vals)  # Fluxo para R ≈ novos recuperados/dia ≈ incidência
t_diario = t[1:]

fig2 = go.Figure()
fig2.add_trace(go.Bar(
    x=t_diario, y=novos_casos,
    name="Novos casos / dia",
    marker_color="#f85149",
    marker_opacity=0.7,
    hovertemplate="Dia: %{x:.0f}<br>Novos casos: %{y:,.0f}<extra></extra>",
))
fig2.add_trace(go.Scatter(
    x=t_diario, y=novos_casos,
    mode="lines",
    line=dict(color="#ff7b72", width=2),
    name="Tendência",
    hoverinfo="skip",
))

fig2.update_layout(
    title=dict(
        text="Incidência Diária — Novos Casos",
        font=dict(family="IBM Plex Mono", size=15, color="#c9d1d9"),
        x=0,
    ),
    plot_bgcolor="#0d1117",
    paper_bgcolor="#0d1117",
    font=dict(family="IBM Plex Sans", color="#8b949e"),
    xaxis=dict(title="Dias", gridcolor="#21262d", zerolinecolor="#21262d",
               tickfont=dict(family="IBM Plex Mono")),
    yaxis=dict(title="Novos Casos", gridcolor="#21262d", zerolinecolor="#21262d",
               tickformat=",", tickfont=dict(family="IBM Plex Mono")),
    legend=dict(bgcolor="#161b22", bordercolor="#21262d", borderwidth=1,
                font=dict(family="IBM Plex Mono", size=12)),
    hovermode="x unified",
    margin=dict(l=60, r=30, t=60, b=50),
    height=320,
    showlegend=True,
)

st.plotly_chart(fig2, use_container_width=True)


# ──────────────────────────────────────────────
# Tabela de resumo por fase (a cada 30 dias)
# ──────────────────────────────────────────────
with st.expander("📊 Tabela de Resumo por Fase (a cada 30 dias)", expanded=False):
    import pandas as pd

    indices_30d = [np.searchsorted(t, d) for d in range(0, int(dias) + 1, 30) if d <= dias]
    dados_tabela = []
    for idx in indices_30d:
        idx = min(idx, len(t) - 1)
        dados_tabela.append({
            "Dia": int(t[idx]),
            "Suscetível (S)": f"{int(S[idx]):,}",
            "Exposto (E)":    f"{int(E[idx]):,}",
            "Infectado (I)":  f"{int(I[idx]):,}",
            "Recuperado (R)": f"{int(R_vals[idx]):,}",
            "% Pop. Afetada": f"{(R_vals[idx]/N*100):.1f}%",
        })

    df = pd.DataFrame(dados_tabela)
    st.dataframe(df, use_container_width=True, hide_index=True)


# ──────────────────────────────────────────────
# Rodapé informativo
# ──────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown("""
<p style="font-size:0.75rem; color:#8b949e; font-family:'IBM Plex Mono',monospace; text-align:center;">
    Simulador SEIR &nbsp;·&nbsp; Scipy <code>odeint</code> &nbsp;·&nbsp; Plotly &nbsp;·&nbsp; Streamlit
    &nbsp;&nbsp;|&nbsp;&nbsp;
    Parâmetros iniciais: E₀ = 1 exposto, I₀ = 0, R₀ inicial = 0
</p>
""", unsafe_allow_html=True)
