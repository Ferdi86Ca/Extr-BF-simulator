import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# 1. DIZIONARIO TRADUZIONI (Incluso OEE, Scarto, TCO)
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
        "capex": "Investment (€)",
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
        "info_msg": "💡 Line B reduces cost per KG by € {:.3f}. Extra profit in 5 years: € {:,.0f}.",
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
        "capex": "Investimento (€)",
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
        "info_msg": "💡 La Linea B riduce il costo al KG di € {:.3f}. Extra profitto in 5 anni: € {:,.0f}.",
        "download_btn": "📩 Scarica Report Professionale"
    }
}

st.set_page_config(page_title="ROI Extrusion Calculator", layout="centered")
lingua_scelta = st.sidebar.selectbox("Select language / Lingua", ["English", "Italiano"])
t = lang_dict[lingua_scelta]

# --- SIDEBAR MERCATO ---
st.sidebar.header(t['sidebar_market'])
costo_pe = st.sidebar.number_input(t['poly_cost'], value=1.40)
prezzo_vendita = st.sidebar.number_input(t['sell_price'], value=2.10)
costo_en = st.sidebar.number_input(t['energy_cost'], value=0.22)
ore_teoriche = st.sidebar.number_input(t['hours'], value=8000)
tol_mercato = st.sidebar.slider(t['market_tol'], 1.0, 10.0, 6.0)

# --- INPUT MACCHINE ---
st.header(t['header_comp'])
col1, col2 = st.columns(2)

with col1:
    st.subheader(t['line_a'])
    c_a = st.number_input(f"{t['capex']} A", value=1500000, key="ca")
    p_a = st.number_input(f"{t['output']} A", value=400, key="pa")
    cons_a = st.number_input(f"{t['cons']} A", value=0.40, key="csa")
    sig_a = st.number_input(f"{t['precision']} A", value=4.5, key="sa")
    m_a = st.number_input(f"{t['maint']} A", value=3.5, key="ma")
    oee_a = st.number_input(f"{t['oee']} A", value=75.0, key="oa")
    scr_a = st.number_input(f"{t['scrap']} A", value=4.0, key="scra")

with col2:
    st.subheader(t['line_b'])
    c_b = st.number_input(f"{t['capex']} B", value=2000000, key="cb")
    p_b = st.number_input(f"{t['output']} B", value=440, key="pb")
    cons_b = st.number_input(f"{t['cons']} B", value=0.35, key="csb")
    sig_b = st.number_input(f"{t['precision']} B", value=1.5, key="sb")
    m_b = st.number_input(f"{t['maint']} B", value=2.0, key="mb")
    oee_b = st.number_input(f"{t['oee']} B", value=85.0, key="ob")
    scr_b = st.number_input(f"{t['scrap']} B", value=1.5, key="scrb")

# --- LOGICA CALCOLO AVANZATA ---
# Ore reali di produzione basate su OEE
ore_eff_a = ore_teoriche * (oee_a / 100)
ore_eff_b = ore_teoriche * (oee_b / 100)

# Produzione Lorda e Netta (meno scarto)
prod_lorda_a = p_a * ore_eff_a
prod_netta_a = prod_lorda_a * (1 - scr_a/100)

prod_lorda_b = p_b * ore_eff_b
prod_netta_b = prod_lorda_b * (1 - scr_b/100)

# Costi Operativi Annui
costo_mat_a = prod_lorda_a * costo_pe
costo_mat_b = prod_lorda_b * costo_pe * (1 - (tol_mercato - sig_b)/100) # Risparmio spessore
costo_en_annuo_a = prod_lorda_a * cons_a * costo_en
costo_en_annuo_b = prod_lorda_b * cons_b * costo_en
costo_maint_annuo_a = c_a * (m_a / 100)
costo_maint_annuo_b = c_b * (m_b / 100)

opex_a = costo_mat_a + costo_en_annuo_a + costo_maint_annuo_a
opex_b = costo_mat_b + costo_en_annuo_b + costo_maint_annuo_b

# Costo al KG (CAPEX ammortizzato 10 anni + OPEX) / Produzione Netta
costo_kg_a = (opex_a + (c_a/10)) / prod_netta_a
costo_kg_b = (opex_b + (c_b/10)) / prod_netta_b

# Margini e ROI
margine_a = (prod_netta_a * prezzo_vendita) - opex_a
margine_b = (prod_netta_b * prezzo_vendita) - opex_b
extra_margine = margine_b - margine_a
payback = (c_b - c_a) / extra_margine if extra_margine > 0 else 0
profitto_5y = (extra_margine * 5) - (c_b - c_a)

# --- VISUALIZZAZIONE ---
st.divider()
st.subheader(t['res_title'])
c1, c2, c3 = st.columns(3)
c1.metric(t['cost_kg'] + " (A)", f"€ {costo_kg_a:.3f}")
c2.metric(t['cost_kg'] + " (B)", f"€ {costo_kg_b:.3f}", delta=f"{costo_kg_b-costo_kg_a:.3f}", delta_color="inverse")
c3.metric(t['payback'], f"{payback:.1f} Yrs")

st.info(t['info_msg'].format(costo_kg_a - costo_kg_b, profitto_5y))

# --- GRAFICO TCO (10 ANNI) ---
st.subheader(t['tco_title'])
tco_a_data = {'Investment': c_a, 'Material (10y)': costo_mat_a*10, 'Energy (10y)': costo_en_annuo_a*10, 'Maint (10y)': costo_maint_annuo_a*10}
tco_b_data = {'Investment': c_b, 'Material (10y)': costo_mat_b*10, 'Energy (10y)': costo_en_annuo_b*10, 'Maint (10y)': costo_maint_annuo_b*10}

col_chart1, col_chart2 = st.columns(2)
with col_chart1:
    fig_a = px.pie(names=list(tco_a_data.keys()), values=list(tco_a_data.values()), title=t['line_a'], hole=0.4)
    st.plotly_chart(fig_a, use_container_width=True)
with col_chart2:
    fig_b = px.pie(names=list(tco_b_data.keys()), values=list(tco_b_data.values()), title=t['line_b'], hole=0.4)
    st.plotly_chart(fig_b, use_container_width=True)

# --- GRAFICO BREAK-EVEN ---
anni = list(range(11))
flusso_a = [-c_a + (margine_a * i) for i in anni]
flusso_b = [-c_b + (margine_b * i) for i in anni]
fig_be = go.Figure()
fig_be.add_trace(go.Scatter(x=anni, y=flusso_a, name=t['line_a'], line=dict(color='gray', dash='dot')))
fig_be.add_trace(go.Scatter(x=anni, y=flusso_b, name=t['line_b'], line=dict(color='#00CC96', width=4)))
st.plotly_chart(fig_be, use_container_width=True)
