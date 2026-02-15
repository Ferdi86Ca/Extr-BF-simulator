import streamlit as st
import plotly.graph_objects as go

# 1. TRADUZIONI
lang_dict = {
    "English": {
        "sidebar_market": "Market Parameters",
        "poly_cost": "Polymer Cost (€/kg)",
        "sell_price": "Film Selling Price (€/kg)",
        "energy_cost": "Energy Cost (€/kWh)",
        "hours": "Theoretical Hours/Year",
        "market_tol": "Market Tolerance (±%)",
        "header_comp": "Line Comparison",
        "line_a": "Line A (Standard)",
        "line_b": "Line B (Premium)",
        "capex": "Investment (€)",
        "output": "Output (kg/h)",
        "cons": "Cons. (kWh/kg)",
        "precision": "2σ Prec. (±%)",
        "maint": "Maint. (%)",
        "oee": "OEE (%)",
        "scrap": "Scrap (%)",
        "res_title": "🏁 ROI & TCO Analysis",
        "extra_margin": "Extra Annual Margin",
        "payback": "Break-even (Years)",
        "cost_kg": "Prod. Cost per KG",
        "profit_5y": "Extra Profit (5y)",
        "tco_title": "TCO 10 Years (€)",
        "info_msg": "💡 Line B saves {:.3f} €/kg. 5y Extra Profit: € {:,.0f}",
        "download_btn": "📩 Download Report"
    },
    "Italiano": {
        "sidebar_market": "Parametri Mercato",
        "poly_cost": "Costo Polimero (€/kg)",
        "sell_price": "Prezzo Vendita (€/kg)",
        "energy_cost": "Costo Energia (€/kWh)",
        "hours": "Ore Teoriche/Anno",
        "market_tol": "Tolleranza Mercato (±%)",
        "header_comp": "Confronto Linee",
        "line_a": "Linea A (Standard)",
        "line_b": "Linea B (Premium)",
        "capex": "Investimento (€)",
        "output": "Portata (kg/h)",
        "cons": "Consumo (kWh/kg)",
        "precision": "Precisione 2σ (±%)",
        "maint": "Manutenzione (%)",
        "oee": "OEE (%)",
        "scrap": "Scarto (%)",
        "res_title": "🏁 Analisi ROI & TCO",
        "extra_margin": "Extra Margine Annuo",
        "payback": "Pareggio (Anni)",
        "cost_kg": "Costo al KG",
        "profit_5y": "Extra Profitto (5 anni)",
        "tco_title": "TCO 10 Anni (€)",
        "info_msg": "💡 Linea B risparmia {:.3f} €/kg. Extra Profitto 5a: € {:,.0f}",
        "download_btn": "📩 Scarica Report"
    }
}

st.set_page_config(page_title="ROI Extrusion", layout="wide")

# Selezione Lingua
lingua = st.sidebar.selectbox("Language / Lingua", ["English", "Italiano"])
t = lang_dict[lingua]

# --- INPUT SIDEBAR ---
st.sidebar.header(t['sidebar_market'])
c_pe = st.sidebar.number_input(t['poly_cost'], value=1.40, format="%.2f")
p_ve = st.sidebar.number_input(t['sell_price'], value=2.10, format="%.2f")
c_en = st.sidebar.number_input(t['energy_cost'], value=0.22, format="%.2f")
h_an = st.sidebar.number_input(t['hours'], value=8000)
tol_m = st.sidebar.slider(t['market_tol'], 1.0, 10.0, 6.0)

# --- INPUT COLONNE ---
st.header(t['header_comp'])
col_a, col_b = st.columns(2)

with col_a:
    st.subheader(t['line_a'])
    ca = st.number_input(f"{t['capex']} A", value=1500000, key="a1")
    pa = st.number_input(f"{t['output']} A", value=400, key="a2")
    csa = st.number_input(f"{t['cons']} A", value=0.40, key="a3")
    sa = st.number_input(f"{t['precision']} A", value=4.5, key="a4")
    ma = st.number_input(f"{t['maint']} A", value=3.5, key="a5")
    oa = st.number_input(f"{t['oee']} A", value=75.0, key="a6")
    scra = st.number_input(f"{t['scrap']} A", value=4.0, key="a7")

with col_b:
    st.subheader(t['line_b'])
    cb = st.number_input(f"{t['capex']} B", value=2000000, key="b1")
    pb = st.number_input(f"{t['output']} B", value=440, key="b2")
    csb = st.number_input(f"{t['cons']} B", value=0.35, key="b3")
    sb = st.number_input(f"{t['precision']} B", value=1.5, key="b4")
    mb = st.number_input(f"{t['maint']} B", value=2.0, key="b5")
    ob = st.number_input(f"{t['oee']} B", value=85.0, key="b6")
    scrb = st.number_input(f"{t['scrap']} B", value=1.5, key="b7")

# --- CALCOLI ---
pra = pa * h_an * (oa/100)
prb = pb * h_an * (ob/100)
neta = pra * (1 - scra/100)
netb = prb * (1 - scrb/100)

mata = pra * c_pe
matb = prb * c_pe * (1 - (tol_m - sb)/100)
enea = pra * csa * c_en
eneb = prb * csb * c_en
mnta = ca * (ma/100)
mntb = cb * (mb/100)

opexa = mata + enea + mnta
opexb = matb + eneb + mntb

ckga = (opexa + (ca/10)) / neta if neta > 0 else 0
ckgb = (opexb + (cb/10)) / netb if netb > 0 else 0
marga = (neta * p_ve) - opexa
margb = (netb * p_ve) - opexb
dmarg = margb - marga
pbk = (cb - ca) / dmarg if dmarg > 0 else 0
p5y = (dmarg * 5) - (cb - ca)

# --- DISPLAY RISULTATI ---
st.markdown("---")
st.title(t['res_title'])

if dmarg <= 0:
    st.error("Marginality of Line B is lower than Line A. ROI cannot be calculated.")
else:
    c1, c2, c3 = st.columns(3)
    c1.metric(t['extra_margin'], f"€ {dmarg:,.0f}")
    c2.metric(t['cost_kg'] + " (B)", f"€ {ckgb:.3f}", delta=f"{ckgb-ckga:.3f}", delta_color="inverse")
    c3.metric(t['profit_5y'], f"€ {p5y:,.0f}")

    st.info(t['info_msg'].format(ckga - ckgb, p5y))

    # TCO PIE CHARTS
    st.subheader(t['tco_title'])
    lbls = ['Investment', 'Material', 'Energy', 'Maintenance']
    
    ga, gb = st.columns(2)
    with ga:
        fig1 = go.Figure(data=[go.Pie(labels=lbls, values=[ca, mata*10, enea*10, mnta*10], hole=.4)])
        fig1.update_layout(title=t['line_a'], showlegend=True)
        st.plotly_chart(fig1, use_container_width=True)
    with gb:
        fig2 = go.Figure(data=[go.Pie(labels=lbls, values=[cb, matb*10, eneb*10, mntb*10], hole=.4)])
        fig2.update_layout(title=t['line_b'], showlegend=True)
        st.plotly_chart(fig2, use_container_width=True)

    # CASH FLOW
    yrs = list(range(11))
    fa = [-ca + (marga * i) for i in yrs]
    fb = [-cb + (margb * i) for i in yrs]
    
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=yrs, y=fa, name=t['line_a'], line=dict(color='gray', dash='dot')))
    fig3.add_trace(go.Scatter(x=yrs, y=fb, name=t['line_b'], line=dict(color='#00CC96', width=4)))
    fig3.add_hline(y=0)
    fig3.update_layout(title="Cash Flow Cumulative", xaxis_title="Years", yaxis_title="€")
    st.plotly_chart(fig3, use_container_width=True)

    report = f"ROI Analysis\nExtra Profit 5y: € {p5y:,.0f}\nCost/kg B: {ckgb:.3f} €"
    st.download_button(t['download_btn'], report, file_name="report.txt")
