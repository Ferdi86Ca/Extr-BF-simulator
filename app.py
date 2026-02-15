import streamlit as st
import plotly.graph_objects as go

# 1. DIZIONARIO DELLE TRADUZIONI
lang_dict = {
    "Italiano": {
        "sidebar_market": "Parametri Mercato",
        "poly_cost": "Costo Polimero (€/kg)",
        "sell_price": "Prezzo Vendita Film (€/kg)",
        "energy_cost": "Costo Energia (€/kWh)",
        "hours": "Ore produzione/anno",
        "market_tol": "Tolleranza Mercato (±%)",
        "header_comp": "Confronto Linee di Estrusione",
        "line_a": "Linea A (Standard)",
        "line_b": "Linea B (Premium)",
        "capex": "Investimento (€)",
        "output": "Portata Oraria (kg/h)",
        "cons": "Consumo (kWh/kg)",
        "precision": "Precisione 2σ (±%)",
        "res_title": "🏁 Analisi del Ritorno (ROI)",
        "extra_margin": "Margine Extra Annuo",
        "payback": "Punto di Pareggio (Anni)",
        "profit_5y": "Extra Profitto (5 anni)",
        "info_msg": "💡 Scegliendo la Linea B, dopo 5 anni avrai generato € {:,.0f} di cassa extra.",
        "chart_profit": "Profitto Cumulativo (€)",
        "download_btn": "📩 Scarica Report"
    },
    "English": {
        "sidebar_market": "Market Parameters",
        "poly_cost": "Polymer Cost (€/kg)",
        "sell_price": "Film Selling Price (€/kg)",
        "energy_cost": "Energy Cost (€/kWh)",
        "hours": "Production Hours/Year",
        "market_tol": "Market Tolerance (±%)",
        "header_comp": "Extrusion Lines Comparison",
        "line_a": "Line A (Standard)",
        "line_b": "Line B (Premium)",
        "capex": "Investment (€)",
        "output": "Hourly Output (kg/h)",
        "cons": "Consumption (kWh/kg)",
        "precision": "2σ Precision (±%)",
        "res_title": "🏁 ROI Analysis",
        "extra_margin": "Extra Annual Margin",
        "payback": "Break-even Point (Years)",
        "profit_5y": "Extra Profit (5 years)",
        "info_msg": "💡 By choosing Line B, after 5 years you will have generated € {:,.0f} in extra cash.",
        "chart_profit": "Cumulative Profit (€)",
        "download_btn": "📩 Download Report"
    },
    "Deutsch": {
        "sidebar_market": "Marktparameter",
        "poly_cost": "Polymerkosten (€/kg)",
        "sell_price": "Filmverkaufspreis (€/kg)",
        "energy_cost": "Energiekosten (€/kWh)",
        "hours": "Betriebsstunden/Jahr",
        "market_tol": "Markttoleranz (±%)",
        "header_comp": "Vergleich der Extrusionslinien",
        "line_a": "Linie A (Standard)",
        "line_b": "Linie B (Premium)",
        "capex": "Investition (€)",
        "output": "Stundenleistung (kg/h)",
        "cons": "Verbrauch (kWh/kg)",
        "precision": "2σ Präzision (±%)",
        "res_title": "🏁 ROI-Analyse",
        "extra_margin": "Zusätzliche Jahresmarge",
        "payback": "Amortisationszeit (Jahre)",
        "profit_5y": "Extra Gewinn (5 Jahre)",
        "info_msg": "💡 Mit Linie B generieren Sie nach 5 Jahren zusätzliche € {:,.0f} an Barmitteln.",
        "chart_profit": "Kumulierter Gewinn (€)",
        "download_btn": "📩 Bericht herunterladen"
    }
}

# 2. SELETTORE LINGUA NELLA SIDEBAR
st.set_page_config(page_title="ROI Extrusion", layout="centered")
st.sidebar.title("🌍 Language / Lingua")
lingua_scelta = st.sidebar.selectbox("Select language", ["Italiano", "English", "Deutsch"])
t = lang_dict[lingua_scelta] # t diventa il nostro "traduttore"

# 3. INTERFACCIA USANDO IL DIZIONARIO
st.title(f"📊 {t['res_title']}")

# Parametri Mercato
st.sidebar.divider()
st.sidebar.header(t['sidebar_market'])
costo_pe = st.sidebar.number_input(t['poly_cost'], value=1.40)
prezzo_vendita = st.sidebar.number_input(t['sell_price'], value=2.10)
costo_en = st.sidebar.number_input(t['energy_cost'], value=0.22)
ore_anno = st.sidebar.number_input(t['hours'], value=7500)
tolleranza_mercato = st.sidebar.slider(t['market_tol'], 1.0, 10.0, 6.0)

# Confronto Macchine
st.header(t['header_comp'])
col1, col2 = st.columns(2)
with col1:
    st.subheader(t['line_a'])
    capex_a = st.number_input(f"{t['capex']} A", value=1500000, key="ca")
    portata_a = st.number_input(f"{t['output']} A", value=400, key="pa")
    cons_a = st.number_input(f"{t['cons']} A", value=0.40, key="csa")
    sigma_a = st.number_input(f"{t['precision']} A", value=4.5, key="sa")
with col2:
    st.subheader(t['line_b'])
    capex_b = st.number_input(f"{t['capex']} B", value=2000000, key="cb")
    portata_b = st.number_input(f"{t['output']} B", value=440, key="pb")
    cons_b = st.number_input(f"{t['cons']} B", value=0.35, key="csb")
    sigma_b = st.number_input(f"{t['precision']} B", value=1.5, key="sb")

# --- LOGICA CALCOLI (Identica a prima) ---
prod_annua_a = portata_a * ore_anno
prod_annua_b = portata_b * ore_anno
risparmio_mat_annuo = prod_annua_b * costo_pe * ((tolleranza_mercato - sigma_b) / 100)
extra_ricavo_prod = (prod_annua_b - prod_annua_a) * (prezzo_vendita - costo_pe)
costo_en_a = prod_annua_a * cons_a * costo_en
costo_en_b = prod_annua_b * cons_b * costo_en
risparmio_energia = costo_en_a - costo_en_b

margine_extra_tot = risparmio_mat_annuo + risparmio_energia + extra_ricavo_prod
payback = (capex_b - capex_a) / margine_extra_tot if margine_extra_tot > 0 else 0
profitto_5y = (margine_extra_tot * 5) - (capex_b - capex_a)

# --- VISUALIZZAZIONE RISULTATI ---
st.divider()
st.subheader(t['res_title'])
c1, c2, c3 = st.columns(3)
c1.metric(t['extra_margin'], f"€ {margine_extra_tot:,.0f}")
c2.metric(t['payback'], f"{payback:.1f}")
c3.metric(t['profit_5y'], f"€ {profitto_5y:,.0f}")

st.info(t['info_msg'].format(profitto_5y))

# Grafico Break-even
anni = [0, 1, 2, 3, 4, 5]
margine_base_a = (prod_annua_a * (prezzo_vendita - costo_pe)) - costo_en_a
margine_base_b = (prod_annua_b * (prezzo_vendita - costo_pe)) - costo_en_b + risparmio_mat_annuo
flusso_a = [-capex_a + (margine_base_a * i) for i in anni]
flusso_b = [-capex_b + (margine_base_b * i) for i in anni]

fig = go.Figure()
fig.add_trace(go.Scatter(x=anni, y=flusso_a, name=t['line_a'], line=dict(color='gray', dash='dot')))
fig.add_trace(go.Scatter(x=anni, y=flusso_b, name=t['line_b'], line=dict(color='#00CC96', width=4)))
fig.update_layout(xaxis_title="Years", yaxis_title=t['chart_profit'])
st.plotly_chart(fig, use_container_width=True)

# Bottone Download
st.download_button(t['download_btn'], f"ROI Analysis: {profitto_5y} €", file_name="report.txt")


