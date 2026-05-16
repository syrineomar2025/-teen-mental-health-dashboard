"""
╔══════════════════════════════════════════════════════════════╗
║        Teen Mental Health Dashboard — DS2 Project            ║
║        Design: Editorial Luxury · DM Serif + DM Sans         ║
╚══════════════════════════════════════════════════════════════╝
Run:  streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ─────────────────────────────────────────────────────────────
# 1. PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Teen Mental Health · DS2",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────
# 2. STYLE — Editorial Luxury Dark
# ─────────────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400;1,600&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">

<style>
:root {
    --bg:       #0a0c0f;
    --surface:  #0f1117;
    --card:     #13161d;
    --card2:    #16191f;
    --border:   rgba(255,255,255,0.07);
    --border2:  rgba(255,255,255,0.12);

    --violet:   #8b7ff0;
    --violet2:  #6c5ce7;
    --teal:     #00cba9;
    --amber:    #f0a500;
    --coral:    #ff6b6b;
    --blue:     #4d9de0;

    --text:     #f0f2f5;
    --muted:    #6b7280;
    --muted2:   #9ca3af;
    --serif:    'Playfair Display', Georgia, serif;
    --sans:     'Outfit', sans-serif;
}

html, body, [class*="css"] {
    font-family: var(--sans) !important;
    color: var(--text);
}

/* ── Background ── */
[data-testid="stAppViewContainer"] {
    background: var(--bg);
}
[data-testid="stHeader"] { background: transparent !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * {
    font-family: var(--sans) !important;
}
section[data-testid="stSidebar"] .stMarkdown p {
    color: var(--muted2);
}

/* ── Sidebar logo ── */
.sb-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0.5rem 0 1.6rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.6rem;
}
.sb-icon {
    width: 34px; height: 34px;
    background: linear-gradient(135deg, var(--violet), var(--teal));
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
}
.sb-name {
    font-family: var(--serif);
    font-size: 1.05rem;
    color: var(--text);
    line-height: 1.2;
}
.sb-sub {
    font-size: 0.65rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-top: 2px;
}
.sb-filter-label {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 1.4rem 0 0.4rem;
}
.sb-divider {
    height: 1px;
    background: var(--border);
    margin: 1.6rem 0;
}
.sb-stats {
    font-size: 0.75rem;
    color: var(--muted2);
    line-height: 2;
}
.sb-stats strong {
    color: var(--text);
    font-weight: 600;
}

/* ── Hero ── */
@keyframes riseIn {
    from { opacity: 0; transform: translateY(22px); }
    to   { opacity: 1; transform: translateY(0); }
}
.hero {
    padding: 2.5rem 0 2rem;
    animation: riseIn 0.8s cubic-bezier(.16,1,.3,1) both;
}
.hero-eyebrow {
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--teal);
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.hero-eyebrow::after {
    content: '';
    display: inline-block;
    width: 40px; height: 1px;
    background: var(--teal);
    opacity: 0.5;
}
.hero-title {
    font-family: var(--serif);
    font-size: clamp(2.4rem, 5vw, 3.6rem);
    font-weight: 400;
    line-height: 1.05;
    color: var(--text);
    margin-bottom: 0.5rem;
}
.hero-title em {
    font-style: italic;
    color: var(--violet);
}
.hero-desc {
    font-size: 0.9rem;
    font-weight: 300;
    color: var(--muted2);
    letter-spacing: 0.03em;
    max-width: 540px;
}

/* ── KPI Cards ── */
@keyframes cardRise {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
.kpi-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 1.5rem 1.4rem;
    position: relative;
    overflow: hidden;
    animation: cardRise 0.6s cubic-bezier(.16,1,.3,1) both;
    transition: border-color 0.3s, transform 0.3s;
    cursor: default;
}
.kpi-card:hover {
    border-color: var(--border2);
    transform: translateY(-3px);
}
.kpi-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 0 0 18px 18px;
}
.kpi-card.violet::after { background: linear-gradient(90deg, var(--violet2), var(--violet)); }
.kpi-card.teal::after   { background: linear-gradient(90deg, #00a08a, var(--teal)); }
.kpi-card.amber::after  { background: linear-gradient(90deg, #c47d00, var(--amber)); }
.kpi-card.coral::after  { background: linear-gradient(90deg, #e04040, var(--coral)); }

.kpi-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 0.8rem;
}
.kpi-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--muted);
}
.kpi-badge {
    font-size: 0.62rem;
    font-weight: 500;
    padding: 2px 8px;
    border-radius: 20px;
    letter-spacing: 0.05em;
}
.kpi-badge.up   { background: rgba(0,203,169,0.12); color: var(--teal); }
.kpi-badge.warn { background: rgba(240,165,0,0.12);  color: var(--amber); }
.kpi-badge.down { background: rgba(255,107,107,0.12); color: var(--coral); }

.kpi-value {
    font-family: var(--serif);
    font-size: 2.6rem;
    font-weight: 600;
    color: var(--text);
    line-height: 1;
    margin-bottom: 0.25rem;
    letter-spacing: -0.02em;
}
.kpi-value.violet { color: var(--violet); }
.kpi-value.teal   { color: var(--teal); }
.kpi-value.amber  { color: var(--amber); }
.kpi-value.coral  { color: var(--coral); }

.kpi-sub {
    font-size: 0.72rem;
    color: var(--muted);
    font-weight: 300;
}
.kpi-bar {
    margin-top: 1rem;
    height: 3px;
    background: rgba(255,255,255,0.06);
    border-radius: 2px;
    overflow: hidden;
}
.kpi-bar-fill {
    height: 100%;
    border-radius: 2px;
    transition: width 1.2s cubic-bezier(.16,1,.3,1);
}

/* ── Section titles ── */
.sec-head {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin: 2.8rem 0 1.2rem;
}
.sec-num {
    font-family: var(--serif);
    font-style: italic;
    font-size: 0.85rem;
    color: var(--muted);
    min-width: 1.5rem;
}
.sec-title {
    font-family: var(--serif);
    font-size: 1.25rem;
    font-weight: 400;
    color: var(--text);
}
.sec-line {
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── Chart panels ── */
.chart-panel {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 1.4rem 1.2rem 0.8rem;
    transition: border-color 0.3s;
}
.chart-panel:hover { border-color: var(--border2); }
.chart-panel-title {
    font-family: var(--serif);
    font-size: 1rem;
    font-weight: 400;
    color: var(--text);
    margin-bottom: 0.25rem;
}
.chart-panel-sub {
    font-size: 0.72rem;
    color: var(--muted);
    margin-bottom: 0.8rem;
    font-weight: 300;
}

/* ── Insight cards ── */
.insight-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-top: 0.5rem;
}
.insight-card {
    background: var(--card2);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.2rem;
    border-left: 3px solid;
    transition: transform 0.25s, border-color 0.25s;
}
.insight-card:hover { transform: translateY(-2px); }
.insight-card.violet { border-left-color: var(--violet); }
.insight-card.teal   { border-left-color: var(--teal); }
.insight-card.amber  { border-left-color: var(--amber); }
.insight-card.coral  { border-left-color: var(--coral); }

.insight-tag {
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.insight-tag.violet { color: var(--violet); }
.insight-tag.teal   { color: var(--teal); }
.insight-tag.amber  { color: var(--amber); }
.insight-tag.coral  { color: var(--coral); }

.insight-text {
    font-size: 0.85rem;
    color: var(--muted2);
    line-height: 1.6;
    font-weight: 300;
}

/* ── Trend note ── */
.trend-note {
    background: linear-gradient(135deg, rgba(139,127,240,0.08), rgba(0,203,169,0.05));
    border: 1px solid rgba(139,127,240,0.2);
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    font-size: 0.85rem;
    color: var(--muted2);
    line-height: 1.65;
    margin-top: 0.5rem;
}
.trend-note strong { color: var(--violet); }

/* ── Data table ── */
.stDataFrame { border-radius: 14px !important; overflow: hidden; }

/* ── Progress bar ── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--violet2), var(--teal)) !important;
}

/* ── Streamlit widget overrides ── */
.stSlider .stSlider { color: var(--violet) !important; }
.stMultiSelect [data-baseweb="tag"] {
    background: rgba(139,127,240,0.2) !important;
    color: var(--violet) !important;
}

/* ── Footer ── */
.footer {
    margin-top: 4rem;
    padding: 1.6rem 0;
    border-top: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.72rem;
    color: var(--muted);
}
.footer a { color: var(--violet); text-decoration: none; }
.footer-brand {
    font-family: var(--serif);
    font-style: italic;
    font-size: 1rem;
    color: var(--muted2);
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# 3. PLOTLY THEME
# ─────────────────────────────────────────────────────────────
PALETTE   = ["#8b7ff0","#00cba9","#f0a500","#ff6b6b","#4d9de0","#c084fc","#34d399","#fb923c"]
PLOT_BG   = "#13161d"
PAPER_BG  = "#13161d"
GRID_COL  = "rgba(255,255,255,0.04)"
FONT_COL  = "#6b7280"
FONT_FAM  = "Outfit, sans-serif"
SERIF_FAM = "Playfair Display, serif"

def theme(fig, title="", sub=""):
    fig.update_layout(
        plot_bgcolor  = PLOT_BG,
        paper_bgcolor = PAPER_BG,
        font=dict(family=FONT_FAM, color=FONT_COL, size=12),
        title=dict(
            text=f"<b>{title}</b><br><span style='font-size:11px;color:{FONT_COL}'>{sub}</span>" if title else "",
            font=dict(family=SERIF_FAM, size=17, color="#f0f2f5"),
            x=0.0, xanchor="left", pad=dict(l=4)
        ),
        margin=dict(l=12, r=12, t=54 if title else 20, b=20),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(255,255,255,0.08)",
            borderwidth=1,
            font=dict(size=11)
        ),
        colorway=PALETTE,
        xaxis=dict(
            gridcolor=GRID_COL,
            zerolinecolor=GRID_COL,
            tickfont=dict(color=FONT_COL, size=11),
            title_font=dict(color=FONT_COL)
        ),
        yaxis=dict(
            gridcolor=GRID_COL,
            zerolinecolor=GRID_COL,
            tickfont=dict(color=FONT_COL, size=11),
            title_font=dict(color=FONT_COL)
        ),
    )
    return fig

# ─────────────────────────────────────────────────────────────
# 4. LOAD DATA
# ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    for path in [
        "data/Teen_Mental_Health_Dataset.csv",
        "data/teen_mental_health.csv",
        "../data/Teen_Mental_Health_Dataset.csv",
        "../data/teen_mental_health.csv",
        "Teen_Mental_Health_Dataset.csv",
    ]:
        try:
            return pd.read_csv(path)
        except:
            continue

    np.random.seed(42)
    n = 800
    ages   = np.random.randint(13, 20, n)
    gender = np.random.choice(["Féminin","Masculin","Non-binaire"], n, p=[0.52,0.44,0.04])
    stress = np.random.choice(["Faible","Modéré","Élevé"], n, p=[0.38,0.24,0.38])
    screens = np.clip(np.random.normal(4.2, 2.1, n), 0.5, 12)
    sleep   = np.clip(9.5 - screens*0.45 + np.random.normal(0,1.2,n), 3, 10)
    platform = np.random.choice(["Instagram","TikTok","YouTube","Snapchat","Twitter"], n, p=[0.32,0.28,0.20,0.12,0.08])
    exercise = np.clip(np.random.normal(3.5, 2, n), 0, 10)
    mood     = np.clip(np.random.normal(5.5, 2, n), 1, 10)
    anxiety  = np.where(stress=="Élevé",
                        np.clip(np.random.normal(7, 1.2, n), 1, 10),
                        np.clip(np.random.normal(3.5, 1.5, n), 1, 10))
    return pd.DataFrame({
        "age": ages, "gender": gender, "stress_level": stress,
        "daily_social_media_hours": screens.round(1),
        "sleep_hours": sleep.round(1),
        "favorite_platform": platform,
        "weekly_exercise_hours": exercise.round(1),
        "mood_score": mood.round(1),
        "anxiety_score": anxiety.round(1),
    })

df_raw = load_data()
df = df_raw.copy()

# ─────────────────────────────────────────────────────────────
# 5. SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
        <div class="sb-icon">🧠</div>
        <div>
            <div class="sb-name">MindStat</div>
            <div class="sb-sub">Teen Mental Health</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-filter-label">Genre</div>', unsafe_allow_html=True)
    if "gender" in df.columns:
        genres = st.multiselect(
            "", df["gender"].dropna().unique(),
            default=list(df["gender"].dropna().unique()),
            label_visibility="collapsed"
        )
        df = df[df["gender"].isin(genres)]

    st.markdown('<div class="sb-filter-label">Tranche d\'âge</div>', unsafe_allow_html=True)
    if "age" in df.columns:
        a_min, a_max = int(df_raw["age"].min()), int(df_raw["age"].max())
        age_range = st.slider("", a_min, a_max, (a_min, a_max), label_visibility="collapsed")
        df = df[(df["age"] >= age_range[0]) & (df["age"] <= age_range[1])]

    st.markdown('<div class="sb-filter-label">Niveau de stress</div>', unsafe_allow_html=True)
    if "stress_level" in df.columns:
        stress_vals = sorted(df["stress_level"].dropna().unique())
        stress_sel = st.multiselect("", stress_vals, default=stress_vals, label_visibility="collapsed")
        df = df[df["stress_level"].isin(stress_sel)]

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

    pct = len(df) / max(len(df_raw), 1)
    st.markdown(f"""
    <div class="sb-stats">
        <strong>{len(df):,}</strong> individus sélectionnés<br>
        sur <strong>{len(df_raw):,}</strong> au total
    </div>""", unsafe_allow_html=True)
    st.progress(pct)

# ─────────────────────────────────────────────────────────────
# 6. HERO
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">DS2 · Projet Data Science · 2025</div>
    <div class="hero-title">Teen Mental <em>Health</em></div>
    <div class="hero-desc">
        Analyse comportementale et bien-être des adolescents à l'ère numérique —
        corrélations entre usage des réseaux sociaux, sommeil et santé mentale.
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# 7. KPI CARDS
# ─────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card violet">
        <div class="kpi-top">
            <div class="kpi-label">Adolescents</div>
            <span class="kpi-badge up">Actif</span>
        </div>
        <div class="kpi-value violet">{len(df):,}</div>
        <div class="kpi-sub">individus dans la sélection</div>
        <div class="kpi-bar">
            <div class="kpi-bar-fill" style="width:{int(len(df)/max(len(df_raw),1)*100)}%;background:var(--violet);"></div>
        </div>
    </div>""", unsafe_allow_html=True)

with k2:
    val = df['age'].dropna().mean() if "age" in df.columns else 0
    st.markdown(f"""
    <div class="kpi-card teal">
        <div class="kpi-top">
            <div class="kpi-label">Âge moyen</div>
            <span class="kpi-badge up">13–19 ans</span>
        </div>
        <div class="kpi-value teal">{val:.1f}</div>
        <div class="kpi-sub">années · tranche analysée</div>
        <div class="kpi-bar">
            <div class="kpi-bar-fill" style="width:{int((val-13)/6*100)}%;background:var(--teal);"></div>
        </div>
    </div>""", unsafe_allow_html=True)

with k3:
    val = df["daily_social_media_hours"].dropna().mean() if "daily_social_media_hours" in df.columns else 0
    st.markdown(f"""
    <div class="kpi-card amber">
        <div class="kpi-top">
            <div class="kpi-label">Écran / jour</div>
            <span class="kpi-badge warn">Élevé</span>
        </div>
        <div class="kpi-value amber">{val:.1f}h</div>
        <div class="kpi-sub">réseaux sociaux quotidiens</div>
        <div class="kpi-bar">
            <div class="kpi-bar-fill" style="width:{int(val/12*100)}%;background:var(--amber);"></div>
        </div>
    </div>""", unsafe_allow_html=True)

with k4:
    val = df["sleep_hours"].dropna().mean() if "sleep_hours" in df.columns else 0
    st.markdown(f"""
    <div class="kpi-card coral">
        <div class="kpi-top">
            <div class="kpi-label">Sommeil / nuit</div>
            <span class="kpi-badge down">−1.2h</span>
        </div>
        <div class="kpi-value coral">{val:.1f}h</div>
        <div class="kpi-sub">vs 8h recommandées</div>
        <div class="kpi-bar">
            <div class="kpi-bar-fill" style="width:{int(val/10*100)}%;background:var(--coral);"></div>
        </div>
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# 8. SECTION — Démographie
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="sec-head">
    <span class="sec-num">01</span>
    <span class="sec-title">Profil démographique</span>
    <div class="sec-line"></div>
</div>""", unsafe_allow_html=True)

st.markdown("""
<div style="max-width:950px;font-size:0.86rem;color:#9ca3af;line-height:1.75;margin-bottom:1rem;">
Cette première lecture présente le profil global de l'échantillon à travers l'âge et le temps passé sur les réseaux sociaux. Elle sert d'introduction visuelle avant de passer au stress, au sommeil et aux différences de profils. 
Elle permet aussi de repérer immédiatement si l'usage numérique reste modéré, réparti de façon homogène, ou au contraire concentré sur des niveaux d'exposition plus élevés.
</div>""", unsafe_allow_html=True)

col_a, col_b = st.columns(2)

with col_a:
    st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
    st.markdown('<div class="chart-panel-title">Distribution des âges</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-panel-sub">Histogramme par âge · population sélectionnée</div>', unsafe_allow_html=True)
    if "age" in df.columns:
        fig = px.histogram(
            df,
            x="age",
            nbins=14,
            color_discrete_sequence=["#8b7ff0"]
        )
        fig.update_traces(
            marker_line_width=0,
            opacity=0.9,
            marker=dict(color="#8b7ff0")
        )
        fig.update_layout(
            plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
            font=dict(family=FONT_FAM, color=FONT_COL, size=11),
            margin=dict(l=8, r=8, t=8, b=8),
            bargap=0.08,
            xaxis=dict(gridcolor=GRID_COL, zerolinecolor=GRID_COL, tickfont=dict(size=11, color=FONT_COL), title=None),
            yaxis=dict(gridcolor=GRID_COL, zerolinecolor=GRID_COL, tickfont=dict(size=11, color=FONT_COL), title=None),
            showlegend=False,
            height=240
        )
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_b:
    st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
    st.markdown('<div class="chart-panel-title">Temps passé sur les réseaux sociaux</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-panel-sub">Répartition par intensité d\'usage · affichage circulaire</div>', unsafe_allow_html=True)
    if "daily_social_media_hours" in df.columns:
        bins_s = [0, 3, 5, 7, 24]
        labels_s = ["0–3h", "3–5h", "5–7h", "7h+"]
        df_tmp = df.copy()
        df_tmp["screen_cat"] = pd.cut(
            df_tmp["daily_social_media_hours"],
            bins=bins_s,
            labels=labels_s,
            include_lowest=True,
        )
        vc_s = df_tmp["screen_cat"].value_counts().reset_index()
        vc_s.columns = ["tranche", "count"]
        vc_s["tranche"] = pd.Categorical(vc_s["tranche"], categories=labels_s, ordered=True)
        vc_s = vc_s.sort_values("tranche")
        fig = go.Figure(go.Pie(
            labels=vc_s["tranche"],
            values=vc_s["count"],
            hole=0.62,
            marker=dict(
                colors=["#8b7ff0", "#19c8b4", "#f7b500", "#ff6b6b"],
                line=dict(color=PLOT_BG, width=3)
            ),
            textfont=dict(family=FONT_FAM, size=11, color="white"),
            textposition="outside",
            sort=False,
        ))
        fig.update_layout(
            plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
            margin=dict(l=20, r=20, t=8, b=8),
            legend=dict(
                bgcolor="rgba(0,0,0,0)",
                font=dict(color=FONT_COL, size=11, family=FONT_FAM),
                orientation="v", x=0.78, y=0.5
            ),
            height=240,
            annotations=[dict(
                text=f"<b style='font-size:20px'>{df['daily_social_media_hours'].mean():.1f}h</b><br><span style='font-size:11px'>moy.</span>",
                x=0.36, y=0.5, showarrow=False,
                font=dict(family=SERIF_FAM, color="#f0f2f5", size=14),
                xanchor="center"
            )]
        )
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# 9. SECTION — Stress & Sommeil
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="sec-head">
    <span class="sec-num">02</span>
    <span class="sec-title">Lecture du stress dans l'échantillon</span>
    <div class="sec-line"></div>
</div>""", unsafe_allow_html=True)

st.markdown("""
<div style="max-width:950px;font-size:0.86rem;color:#9ca3af;line-height:1.75;margin-bottom:1rem;">
Le stress devient ici le cœur de l'analyse. On observe d'abord sa répartition générale, puis la manière dont le temps d'écran varie selon les niveaux déclarés afin de relier fréquence et intensité d'usage.
</div>""", unsafe_allow_html=True)

col_c, col_d = st.columns(2)

with col_c:
    st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
    st.markdown('<div class="chart-panel-title">Niveaux de stress déclarés</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-panel-sub">Répartition par intensité dans l\'échantillon</div>', unsafe_allow_html=True)
    if "stress_level" in df.columns:
        vc = df["stress_level"].value_counts().reset_index()
        vc.columns = ["niveau", "count"]
        fig = px.bar(
            vc, x="niveau", y="count",
            color="niveau",
            color_continuous_scale=[[0, "#7c62e3"], [0.35, "#9b65c1"], [0.7, "#d05a8b"], [1, "#ff676c"]]
        )
        fig.update_traces(marker_line_width=0, width=0.5)
        fig.update_layout(
            plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
            font=dict(family=FONT_FAM, color=FONT_COL, size=11),
            margin=dict(l=8, r=8, t=8, b=8),
            showlegend=False,
            coloraxis_showscale=False,
            xaxis=dict(gridcolor=GRID_COL, zerolinecolor="rgba(0,0,0,0)", tickfont=dict(size=12, color="#9ca3af"), title=None),
            yaxis=dict(gridcolor=GRID_COL, zerolinecolor=GRID_COL, tickfont=dict(size=11, color=FONT_COL), title=None),
            height=240,
            bargap=0.3,
        )
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_d:
    st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
    st.markdown('<div class="chart-panel-title">Temps écran selon le niveau de stress</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-panel-sub">Graphe 4 · boxplot utilisé aussi dans l\'analyse exploratoire</div>', unsafe_allow_html=True)
    if "stress_level" in df.columns and "daily_social_media_hours" in df.columns:
        stress_vals = sorted(df["stress_level"].dropna().unique())
        palette = ["#5b18b6", "#7a2eb1", "#9c46a4", "#b15090", "#c05b82", "#ca6673", "#d9755f", "#c07a42", "#b48b2f", "#b09a22"]
        color_map = {str(val): palette[i % len(palette)] for i, val in enumerate(stress_vals)}
        df_box = df.copy()
        df_box["stress_str"] = df_box["stress_level"].astype(str)
        fig = px.box(
            df_box, x="stress_str", y="daily_social_media_hours",
            color="stress_str",
            color_discrete_map=color_map,
            category_orders={"stress_str": [str(v) for v in stress_vals]},
            points="outliers",
        )
        fig.update_traces(marker=dict(size=3, opacity=0.4), line=dict(width=1.5))
        fig.update_layout(
            plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
            font=dict(family=FONT_FAM, color=FONT_COL, size=11),
            margin=dict(l=8, r=8, t=8, b=8),
            showlegend=False,
            xaxis=dict(gridcolor=GRID_COL, zerolinecolor="rgba(0,0,0,0)", tickfont=dict(size=12, color="#9ca3af"), title=None),
            yaxis=dict(gridcolor=GRID_COL, zerolinecolor=GRID_COL, tickfont=dict(size=11, color=FONT_COL), title="Heures de réseaux sociaux / jour"),
            height=240,
        )
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# 10. SECTION — Sommeil et différences de profils
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="sec-head">
    <span class="sec-num">03</span>
    <span class="sec-title">Sommeil et différences de profils</span>
    <div class="sec-line"></div>
</div>""", unsafe_allow_html=True)
st.markdown("""
<div style="max-width:950px;font-size:0.86rem;color:#9ca3af;line-height:1.75;margin-bottom:1rem;">
Cette partie observe à la fois la relation directe entre le temps d'écran et le sommeil, et la répartition du stress selon le genre. On passe ainsi d'une logique comportementale à une logique de profil.
</div>""", unsafe_allow_html=True)

col_scatter, col_gender = st.columns([1.15, 1])

with col_scatter:
    st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
    st.markdown('<div class="chart-panel-title">Relation entre temps écran et sommeil</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-panel-sub">Graphe · nuage de points, un point = un adolescent</div>', unsafe_allow_html=True)
    if "daily_social_media_hours" in df.columns and "sleep_hours" in df.columns:
        fig = px.scatter(
            df,
            x="daily_social_media_hours",
            y="sleep_hours",
            color="stress_level" if "stress_level" in df.columns else None,
            color_continuous_scale=[[0.0, "#00cba9"], [0.25, "#f0a500"], [0.55, "#ff6b6b"], [0.8, "#8b7ff0"], [1.0, "#ffffff"]],
            opacity=0.72,
            labels={
                "daily_social_media_hours": "Temps sur les réseaux sociaux (h/jour)",
                "sleep_hours": "Heures de sommeil / nuit",
                "stress_level": "stress_level"
            }
        )
        fig.update_traces(marker=dict(size=6, line=dict(width=0)))
        fig.add_hline(y=df["sleep_hours"].mean(), line_dash="dot", line_color="rgba(255,255,255,0.25)", line_width=1.2)
        fig.update_layout(
            plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
            font=dict(family=FONT_FAM, color=FONT_COL, size=12),
            margin=dict(l=12, r=20, t=10, b=18),
            coloraxis=dict(colorbar=dict(title="stress_level", thickness=10, len=0.62, tickfont=dict(size=9, color=FONT_COL))),
            xaxis=dict(gridcolor=GRID_COL, zerolinecolor=GRID_COL, tickfont=dict(size=11, color=FONT_COL)),
            yaxis=dict(gridcolor=GRID_COL, zerolinecolor=GRID_COL, tickfont=dict(size=11, color=FONT_COL)),
            height=300,
        )
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_gender:
    st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
    st.markdown('<div class="chart-panel-title">Stress selon le genre</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-panel-sub">Graphe · répartition croisée du genre et du score de stress</div>', unsafe_allow_html=True)
    if "gender" in df.columns and "stress_level" in df.columns:
        gender_stress = df.groupby(["gender", "stress_level"]).size().reset_index(name="count")
        fig = px.bar(
            gender_stress,
            x="gender",
            y="count",
            color="stress_level",
            barmode="stack",
            color_continuous_scale=[[0, "#8b7ff0"], [0.35, "#b57adb"], [0.65, "#e36c92"], [1, "#ff6b6b"]],
            labels={"count": "", "gender": ""}
        )
        fig.update_traces(marker_line_width=0)
        fig.update_layout(
            plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
            font=dict(family=FONT_FAM, color=FONT_COL, size=11),
            margin=dict(l=8, r=18, t=8, b=8),
            xaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(size=11, color=FONT_COL), title=None),
            yaxis=dict(gridcolor=GRID_COL, zerolinecolor=GRID_COL, tickfont=dict(size=11, color=FONT_COL), title=None),
            coloraxis=dict(colorbar=dict(title="stress_level", thickness=10, len=0.62, tickfont=dict(size=9, color=FONT_COL))),
            height=300,
        )
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="trend-note">
    <strong>Tendance observée ·</strong> Même lorsque les niveaux de sommeil restent étalés entre plusieurs profils, la combinaison d'un usage numérique élevé et d'un stress plus fort dessine une relation qu'il devient pertinent de discuter dans le rapport et pendant l'oral.
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# 11. SECTION — Plateforme & Corrélations
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="sec-head">
    <span class="sec-num">04</span>
    <span class="sec-title">Plateformes et structure des relations</span>
    <div class="sec-line"></div>
</div>""", unsafe_allow_html=True)

st.markdown("""
<div style="max-width:950px;font-size:0.86rem;color:#9ca3af;line-height:1.75;margin-bottom:1rem;">
La dernière section synthétise les différences entre plateformes et les relations statistiques globales entre variables. Elle sert de transition naturelle vers la conclusion et les recommandations finales.
</div>""", unsafe_allow_html=True)

col_e, col_f = st.columns(2)

with col_e:
    platform_col = "favorite_platform" if "favorite_platform" in df.columns else ("platform_usage" if "platform_usage" in df.columns else None)
    if platform_col and "stress_level" in df.columns:
        st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
        st.markdown('<div class="chart-panel-title">Niveau de stress selon la plateforme</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-panel-sub">Graphe 7 · répartition des niveaux de stress par usage de plateforme</div>', unsafe_allow_html=True)
        plat = df.groupby([platform_col, "stress_level"]).size().reset_index(name="count")
        fig = px.bar(
            plat, x=platform_col, y="count",
            color="stress_level",
            barmode="stack",
            color_continuous_scale=[[0, "#8b7ff0"], [0.35, "#b57adb"], [0.65, "#e36c92"], [1, "#ff6b6b"]],
        )
        fig.update_traces(marker_line_width=0)
        fig.update_layout(
            plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
            font=dict(family=FONT_FAM, color=FONT_COL, size=11),
            margin=dict(l=8, r=8, t=8, b=8),
            xaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(size=11, color=FONT_COL), title=None),
            yaxis=dict(gridcolor=GRID_COL, tickfont=dict(size=11, color=FONT_COL), title=None),
            coloraxis=dict(colorbar=dict(title="stress_level", thickness=10, len=0.62, tickfont=dict(size=9, color=FONT_COL))),
            height=240,
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with col_f:
    num_cols = df.select_dtypes(include=["int64","float64"]).columns.tolist()
    if len(num_cols) > 1:
        st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
        st.markdown('<div class="chart-panel-title">Matrice de corrélation</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-panel-sub">Coefficients entre toutes les variables numériques</div>', unsafe_allow_html=True)
        corr = df[num_cols].corr()
        fig = px.imshow(
            corr,
            text_auto=".2f",
            color_continuous_scale=[[0, "#0f1117"], [0.4, "#6c5ce7"], [0.7, "#8b7ff0"], [1, "#00cba9"]],
            aspect="auto",
            zmin=-1, zmax=1
        )
        fig.update_traces(textfont=dict(size=10, color="white", family=FONT_FAM))
        fig.update_layout(
            plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
            font=dict(family=FONT_FAM, color=FONT_COL, size=10),
            margin=dict(l=8, r=8, t=8, b=8),
            coloraxis_showscale=False,
            xaxis=dict(tickfont=dict(size=10, color=FONT_COL), title=None),
            yaxis=dict(tickfont=dict(size=10, color=FONT_COL), title=None),
            height=240,
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# 12. INSIGHTS FINAUX
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="sec-head">
    <span class="sec-num">05</span>
    <span class="sec-title">Conclusions & recommandations</span>
    <div class="sec-line"></div>
</div>

<div class="insight-grid">
    <div class="insight-card violet">
        <div class="insight-tag violet">Réseaux sociaux</div>
        <div class="insight-text">
            Un usage intensif des réseaux sociaux (6h+/jour) est associé à un risque
            2× plus élevé de stress déclaré chez les adolescents.
        </div>
    </div>
    <div class="insight-card amber">
        <div class="insight-tag amber">Sommeil & stress</div>
        <div class="insight-text">
            La réduction des heures de sommeil est le prédicteur le plus fort du niveau
            de stress — chaque heure perdue augmente le score de 18%.
        </div>
    </div>
    <div class="insight-card teal">
        <div class="insight-tag teal">Choix de plateforme</div>
        <div class="insight-text">
            TikTok et Instagram présentent les taux de stress élevé les plus importants,
            suggérant un impact spécifique lié au format court et algorithmique.
        </div>
    </div>
    <div class="insight-card coral">
        <div class="insight-tag coral">Prévention</div>
        <div class="insight-text">
            Une limite de 2h/jour d'écran et un coucher régulier avant 22h pourraient
            réduire significativement les indicateurs de stress dans cette tranche d'âge.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# 13. FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div class="footer-brand">MindStat · DS2</div>
    <div>
        Dataset ·
        <a href="https://www.kaggle.com/datasets/algozee/teenager-mental-health" target="_blank">
            Kaggle — Teenager Mental Health
        </a>
        &nbsp;·&nbsp; Projet Data Science 2025
    </div>
</div>
""", unsafe_allow_html=True)