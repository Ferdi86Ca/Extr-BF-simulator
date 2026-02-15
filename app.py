import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# 1. DIZIONARIO TRADUZIONI
lang_dict = {
    "English": {
        "sidebar_market": "Market Parameters",
        "poly_cost": "Polymer Cost (€/kg)",
        "sell_price": "Film Selling Price (€/kg)",
        "energy_cost": "Energy Cost (€/kWh)",
        "hours": "Theoretical Hours/Year",
        "market_tol": "Market Tolerance (±%)",
        "header_comp": "Extrusion Lines Comparison",
        "line_a": "Line A (Standard)",
        "line_b": "Line B (Premium)",
        "capex": "Investment (M€)",
        "output": "Hourly Output (kg/h)",
        "cons": "Consumption (kWh/kg)",
        "precision": "2σ Precision (±%)",
        "maint": "Annual Maintenance (%)",
        "oee": "OEE - Efficiency (%)",
        "scrap": "Scrap Rate (%)",
        "res_title": "🏁 ROI & TCO Analysis",
        "extra_margin": "Extra Annual Margin",
        "payback": "Break-even (Years)",
        "cost_kg": "Production Cost per KG",
        "profit_5y": "Extra Profit (5 years)",
        "tco_title": "Total Cost of Ownership (10 Years)",
        "info_msg": "💡 Line B reduces cost per KG by € {:.3f}. Extra profit in 5 years: € {:,.2f} M",
        "download_btn": "📩 Download Professional Report"
    },
    "Italiano": {
        "sidebar_market": "Parametri Mercato",
        "poly_cost": "Costo Polimero (€/kg)",
        "sell_price": "Prezzo Vendita Film (€/kg)",
        "energy_cost": "Costo Energia (€/kWh)",
        "hours": "Ore Teoriche/Anno",
        "market_tol": "Tolleranza Mercato (±%)",
        "header_comp": "Confronto Linee di Estrusione",
        "line_a": "Linea A (Standard)",
        "line_b": "Linea B (Premium)",
        "capex": "Investimento (M€)",
        "output": "Portata Oraria (kg/h)",
        "cons": "Consumo (kWh/kg)",
        "precision": "Precisione 2σ (±%)",
        "maint": "Manutenzione Annua (%)",
        "oee": "OEE - Efficienza (%)",
        "scrap": "Percentuale Scarto (%)",
        "res_title": "🏁 Analisi ROI & TCO",
        "extra_margin": "Margine Extra Annuo",
        "payback": "Punto di Pareggio (Anni)",
        "cost_kg": "Costo Produzione al KG",
        "profit_5y": "Extra Profitto (5 anni)",
        "tco_title": "Total Cost of Ownership (10 Anni)",
        "info_msg": "💡 La Linea B riduce il costo al KG di € {:.3f}. Extra profitto in 5 anni: € {:,.2f} M",
        "download_btn": "📩 Scarica Report Professionale"
    }
}

st.set_page_config(page_title="ROI Extrusion Calculator", layout="centered")
lingua_scelta = st.sidebar.selectbox("Select language / Lingua", ["English", "Italiano"])
t = lang_dict[lingua_scelta]

# --- SIDEBAR MERCATO ---
st.sidebar.header(t['sidebar_market'])
costo_pe = st.sidebar.number_input(t['poly_cost'], value=1.40, step=0.05)
prezzo_vendita = st.sidebar.number_input(t['sell_price'], value=2.10, step=0.05)
costo_en = st.sidebar.number_input(t['energy_cost'], value=0.22, step=0.01)
ore_teoriche = st.sidebar.number_input(t['hours'], value=8000, step=100)
tol_mercato = st.sidebar.slider(t['market_tol'], 1.0, 10.0, 6.0)

# --- INPUT MACCHINE (Conversione M€ -> €) ---
st.header(t['header_comp'])
col1, col2 = st.columns(2)

with col1:
    st.subheader(t['line_a'])
    c_a_m = st.number_input(f"{t['capex']} A", value=1.50, step=0.05, key="ca_m")
    c_a = c_a_m * 1_000_000 # Conversione interna
    p_a = st.number_input(f"{t['output']} A", value=400, key="pa")
    cons_a = st.number_input(f"{t['cons']} A", value=0.40, key="csa")
    sig_a = st.number_input(f"{t['precision']} A", value=4.5, key="sa")
    m_a = st.number_input(f"{t['maint']} A", value=3.5, key="ma")
    oee_a = st.number_input(f"{t['oee']} A", value=75.0, key="oa")
    scr_a = st.number_input(f"{t['scrap']} A", value=4.0, key="scra")

with col2:
    st.subheader(t['line_b'])
    c_b_m = st.number_input(f"{t['capex']} B", value=2.00, step=0.05, key="cb_m")
    c_b = c_b_m * 1_000_000 # Conversione interna
    p_b = st.number_input(f"{t['output']} B", value=440, key="pb")
    cons_b = st
