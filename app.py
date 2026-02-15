import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# 1. DIZIONARIO TRADUZIONI MULTILINGUA
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
        "cons": "Consumption (kWh/kg)",
        "precision": "2σ Precision (±%)",
        "maint": "Maint. (%)",
        "oee": "OEE Efficiency (%)",
        "scrap": "Scrap Rate (%)",
        "res_title": "🏁 ROI Analysis Results",
        "tech_comp": "📊 Comparative Performance Table",
        "extra_margin": "Extra Annual Margin",
        "payback": "Payback (Years)",
        "cost_kg": "Prod. Cost per KG",
        "profit_5y": "Extra Profit (5y)",
        "info_msg": "💡 Line B reduces cost per KG by € {:.3f}. Extra profit in 5 years: € {:,.0f}",
        "download_btn": "📩 Download Report",
        "diff_col": "Difference (B vs A)"
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
        "oee": "OEE - Efficienza (%)",
        "scrap": "Percentuale Scarto (%)",
        "res_title": "🏁 Risultati Analisi ROI",
        "tech_comp": "📊 Tabella Comparativa Prestazioni",
        "extra_margin": "Extra Margine Annuo",
        "payback": "Pareggio (Anni)",
        "cost_kg": "Costo al KG",
        "profit_5y": "Extra Profitto (5 anni)",
        "info_msg": "💡 La Linea B riduce il costo al KG di € {:.3f}. Extra profitto in 5 anni: € {:,.0f}",
        "download_btn": "📩 Scarica Report",
        "diff_col": "Differenza (B vs A)"
    },
    "Deutsch": {
        "sidebar_market": "Marktparameter",
        "poly_cost": "Polymerpreis (€/kg)",
        "sell_price": "Verkaufspreis Film (€/kg)",
        "energy_cost": "Energiekosten (€/kWh)",
        "hours": "Theoretische Std/Jahr",
        "market_tol": "Markttoleranz (±%)",
        "header_comp": "Linienvergleich",
        "line_a": "Linie A (Standard)",
        "line_b": "Linie B (Premium)",
        "capex": "Investition (€)",
        "output": "Ausstoß (kg/h)",
        "cons": "Verbrauch (kWh/kg)",
        "precision": "2σ Präzision (±%)",
        "maint": "Wartung (%)",
        "oee": "OEE Effizienz (%)",
        "scrap": "Ausschussrate (%)",
        "res_title": "🏁 ROI-Analyseergebnisse",
        "tech_comp": "📊 Vergleichstabelle der Leistung",
        "extra_margin": "Zusätzliche Jahresmarge",
        "payback": "Amortisation (Jahre)",
        "cost_kg": "Prod.-Kosten pro KG",
        "profit_5y": "Extra Profit (5 J.)",
        "info_msg": "💡 Linie B senkt die Kosten pro KG um € {:.3f}. Extra Profit in 5 Jahren: € {:,.0f}",
        "download_btn": "📩 Bericht Herunterladen",
        "diff_col": "Differenz (B vs A)"
    },
    "Español": {
        "sidebar_market": "Parámetros de Mercado",
        "poly_cost": "Costo Polímero (€/kg)",
        "sell_price": "Precio Venta Film (€/kg)",
        "energy_cost": "Costo Energía (€/kWh)",
        "hours": "Horas Teóricas/Año",
        "market_tol": "Tolerancia Mercado (±%)",
        "header_comp": "Comparación de Líneas",
        "line_a": "Línea A (Estándar)",
        "line_b": "Línea B (Premium)",
        "capex": "Inversión (€)",
        "output": "Rendimiento (kg/h)",
        "cons": "Consumo (kWh/kg)",
        "precision": "Precisión 2σ (±%)",
        "maint": "Mantenimiento (%)",
        "oee": "OEE Eficiencia (%)",
        "scrap": "Tasa de Desperdicio (%)",
        "res_title": "🏁 Resultados del Análisis ROI",
        "tech_comp": "📊 Tabla Comparativa de Rendimiento",
        "extra_margin": "Margen Anual Extra",
        "payback": "Retorno (Años)",
        "cost_kg": "Costo Prod. por KG",
        "profit_5y": "Extra Beneficio (5a)",
        "info_msg": "💡 La Línea B reduce el costo por KG en € {:.3f}. Beneficio extra en 5 años: € {:,.0f}",
        "download_btn": "📩 Descargar Informe",
        "diff_col": "Diferencia (B vs A)"
    }
}

st.set_page_config(page_title="ROI Extrusion", layout="wide")

# Selezione Lingua (English prima)
lingua = st.sidebar.selectbox("Language / Sprache / Idioma", ["English", "Italiano", "Deutsch", "Español"])
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

# --- TABELLA COMPARATIVA ---
st.markdown("---")
st.subheader(t['tech_comp'])

data = {
    "Parameter": [t['capex'], t['output'], t['oee'], t['scrap'], t['cons'], t['cost_kg'], t['extra_margin']],
    t['line_a']: [f"€ {ca:,.0f}", f"{pa} kg/h", f"{oa}%", f"{scra}%", f"{csa} kWh/kg", f"€ {ckga:.3f}", f"€ {marga:,.0f}"],
    t['line_b']: [f"€ {cb:,.0f}", f"{pb} kg/h", f"{ob}%", f"{scrb}%", f"{csb} kWh/kg", f"€ {ckgb:.3f}", f"€ {margb:,.0f}"],
    t['diff_col']: [
        f"🔴 +€ {cb-ca:,.0f}", 
        f"📈 +{pb-pa} kg/h", 
        f"✅ +{ob-oa}%", 
        f"📉 {scrb-scra}%", 
        f"📉 {csb-csa:.2f} kWh/kg", 
        f"✅ -€ {ckga-ckgb:.3f}", 
        f"🔥 +€ {dmarg:,.0f}"
    ]
}
df = pd.DataFrame(data)
st.table(df)

# --- DISPLAY RISULTATI ROI ---
st.title(t['res_title'])

if dmarg <= 0:
    st.error("Marginality of Line B is lower than Line A. ROI cannot be calculated.")
else:
    c1, c2, c3 = st.columns(3)
    c1.metric(t['extra_margin'], f"€ {dmarg:,.0f}")
    c2.metric(t['payback'], f"{pbk:.1f} Yrs")
    c3.metric(t['profit_5y'], f"€ {p5y:,.0f}")

    st.info(t['info_msg'].format(ckga - ckgb, p5y))

    # GRAFICO CASH FLOW
    yrs = list(range(11))
    fa = [-ca + (marga * i) for i in yrs]
    fb = [-cb + (margb * i) for i in yrs]
    
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=yrs, y=fa, name=t['line_a'], line=dict(color='gray', dash='dot')))
    fig3.add_trace(go.Scatter(x=yrs, y=fb, name=t['line_b'], line=dict(color='#00CC96', width=4)))
    fig3.add_hline(y=0, line_color="black")
    fig3.update_layout(title="Cumulative Cash Flow (10 Years)", xaxis_title="Years", yaxis_title="€ Cash Flow", height=500)
    st.plotly_chart(fig3, use_container_width=True)

    # Bottone Report
    report = f"Analysis - {lingua}\n\nExtra Profit 5y: € {p5y:,.0f}\nPayback: {pbk:.1f} years\nCost/kg B: {ckgb:.3f} €"
    st.download_button(t['download_btn'], report, file_name=f"ROI_{lingua}.txt")
