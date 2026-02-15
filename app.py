import streamlit as st
import plotly.graph_objects as go

# 1. DIZIONARIO TRADUZIONI
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

st.set_page_config(page_title="ROI Extrusion Calculator", layout="centered")
lingua_scelta = st.sidebar.selectbox("Language / Lingua", ["English", "Italiano"])
t = lang_dict[lingua_scelta]

# --- SIDEBAR MERCATO ---
st.sidebar.header(t['sidebar_market'])
c_pe = st.sidebar.number_input(t['poly_cost'], value=1.40, step=0.05, format="%.2f")
p_ve = st.sidebar.number_input(t['sell_price'], value=2.10, step=0.05, format="%.2f")
c_en = st.sidebar.number_input(t['energy_cost'], value=0.22, step=0.01, format="%.2f")
h_an = st.sidebar.number_input(t['hours'], value=8000, step=100)
tol_m = st.sidebar.slider(t['market_tol'], 1.0, 10.0, 6.0)

# --- INPUT MACCHINE (Valori Interi Precisi) ---
st.header(t['header_comp'])
col1, col2 = st.columns(2)

with col1:
    st.subheader(t['line_a'])
    ca = st.number_input(f"{t['capex']} A", value=1500000, step=1000, key="ka1")
    pa = st.number_input(f"{t['output']} A", value=400, key="ka2")
    csa = st.number_input(f"{t['cons']} A", value=0.40, key="ka3")
    sa = st.number_input(f"{t['precision']} A", value=4.5, key="ka4")
    ma = st.number_input(f"{t['maint']} A", value=3.5, key="ka5")
    oa = st.number_input(f"{t['oee']} A", value=75.0, key="ka6")
    scra = st.number_input(f"{t['scrap']} A", value=4.0, key="ka7")

with col2:
    st.subheader(t['line_b'])
    cb = st.number_input(f"{t['capex']} B", value=2000000, step=1000, key="kb1")
    pb = st.number_input(f"{t['output']} B", value=440, key="kb2")
    csb = st.number_input(f"{t['cons']} B", value=0.35, key="kb3")
    sb = st.number_input(f"{t['precision']} B", value=1.5, key="kb4")
    mb = st.number_input(f"{t['maint']} B", value=2.0, key="kb5")
    ob = st.number_input(f"{t['oee']} B", value=85.0, key="kb6")
    scrb = st.number_input(f"{t['scrap']} B", value=1.5, key="kb7")

# --- CALCOLI ---
pr_a = (pa * h_an * (oa/100))
pr_b = (pb * h_an * (ob/100))
net_a = pr_a * (1 - scra/100)
net_b = pr_b * (1 - scrb/100)

mat_a = pr_a * c_pe
mat_b = pr_b * c_pe * (1 - (tol_m - sb)/100)
ene_a = pr_a * csa * c_en
ene_b = pr_b * csb * c_en
mnt_a = ca * (ma/100)
mnt_b = cb * (mb/100)

opex_a = mat_a + ene_a + mnt_a
opex_b = mat_b + ene_b + mnt_b

cost_kg_a = (opex_a + (ca/10)) / net_a
cost_kg_b = (opex_b + (cb/10))
