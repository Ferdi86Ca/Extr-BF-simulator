import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# 1. DIZIONARIO TRADUZIONI COMPLETO
lang_dict = {
    "English": {
        "sidebar_market": "Market Parameters",
        "currency_settings": "Currency Settings",
        "exchange_rate": "Exchange Rate (1€ = X $)",
        "poly_cost": "Polymer Cost",
        "sell_price": "Film Selling Price",
        "energy_cost": "Energy Cost",
        "hours": "Theoretical Hours/Year",
        "market_tol": "Market Tolerance (±%)",
        "header_comp": "Line Comparison",
        "line_a": "Line A (Standard)",
        "line_b": "Line B (Premium)",
        "capex": "Investment",
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
        "info_msg": "💡 Line B reduces cost per KG by {} {:.3f}. Extra profit in 5 years: {} {:,.0f}",
        "download_btn": "📩 Download Strategic Report",
        "diff_col": "Difference (B vs A)"
    },
    "Italiano": {
        "sidebar_market": "Parametri Mercato",
        "currency_settings": "Impostazioni Valuta",
        "exchange_rate": "Tasso di Cambio (1€ = X $)",
        "poly_cost": "Costo Polimero",
        "sell_price": "Prezzo Vendita",
        "energy_cost": "Costo Energia",
        "hours": "Ore Teoriche/Anno",
        "market_tol": "Tolleranza Mercato (±%)",
        "header_comp": "Confronto Linee",
        "line_a": "Linea A (Standard)",
        "line_b": "Linea B (Premium)",
        "capex": "Investimento",
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
        "info_msg": "💡 La Linea B riduce il costo al KG di {} {:.3f}. Extra profitto in 5 anni: {} {:,.0f}",
        "download_btn": "📩 Scarica Report Strategico",
        "diff_col": "Differenza (B vs A)"
    },
    "Deutsch": {
        "sidebar_market": "Marktparameter",
        "currency_settings": "Währungseinstellungen",
        "exchange_rate": "Wechselkurs (1€ = X $)",
        "poly_cost": "Polymerpreis",
        "sell_price": "Verkaufspreis Film",
        "energy_cost": "Energiekosten",
        "hours": "Theoretische Std/Jahr",
        "market_tol": "Markttoleranz (±%)",
        "header_comp": "Linienvergleich",
        "line_a": "Linie A (Standard)",
        "line_b": "Linie B (Premium)",
        "capex": "Investition",
        "output": "Ausstoß (kg/h)",
        "cons": "Verbrauch (kWh/kg)",
        "precision": "2σ Präzision (±%)",
        "maint": "Wartung (%)",
        "oee": "OEE Effizienz (%)",
        "scrap": "Ausschussrate (%)",
        "res_title": "🏁 ROI-Analyseergebnisse",
        "tech_comp": "📊 Leistungsvergleichstabelle",
        "extra_margin": "Zusätzliche Jahresmarge",
        "payback": "Amortisation (Jahre)",
        "cost_kg": "Prod.-Kosten pro KG",
        "profit_5y": "Extra Profit (5 J.)",
        "info_msg": "💡 Linie B senkt die Kosten pro KG um {} {:.3f}. Extra Profit in 5 Jahren: {} {:,.0f}",
        "download_btn": "📩 Strategischen Bericht herunterladen",
        "diff_col": "Differenz (B vs A)"
    },
    "Español": {
        "sidebar_market": "Parámetros de Mercado",
        "currency_settings": "Configuración de Moneda",
        "exchange_rate": "Tipo de Cambio (1€ = X $)",
        "poly_cost": "Costo Polímero",
        "sell_price": "Precio Venta Film",
        "energy_cost": "Costo Energía",
        "hours": "Horas Teóricas/Año",
        "market_tol": "Tolerancia Mercado (±%)",
        "header_comp": "Comparativa de Líneas",
        "line_a": "Línea A (Estándar)",
        "line_b": "Línea B (Premium)",
        "capex": "Inversión",
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
        "info_msg": "💡 La Línea B reduce el costo por KG en {} {:.3f}. Beneficio extra en 5 años: {} {:,.0f}",
        "download_btn": "📩 Descargar Informe Estratégico",
        "diff_col": "Diferencia (B vs A)"
    }
}

st.set_page_config(page_title="ROI Extrusion Multi-Lang", layout="wide")

# Selezione Lingua (Ordine richiesto)
lingua = st.sidebar.selectbox("Language / Lingua / Sprache / Idioma", ["English", "Italiano", "Deutsch", "Español"])
t = lang_dict[lingua]

# --- CURRENCY ---
st.sidebar.divider()
st.sidebar.header(t['currency_settings'])
valuta_sel = st.sidebar.radio("Currency / Valuta", ["EUR (€)", "USD ($)"])
cambio = 1.0
simbolo = "€"
val_code = "EUR"

if "USD" in valuta_sel:
    cambio = st.sidebar.number_input(t['exchange_rate'], value=1.08, format="%.2f")
    simbolo = "$"
    val_code = "USD"

# --- INPUT SIDEBAR ---
st.sidebar.header(t['sidebar_market'])
c_pe = st.sidebar.number_input(f"{t['poly_cost']} ({simbolo}/kg)", value=1.40 * cambio, format="%.2f") / cambio
p_ve = st.sidebar.number_input(f"{t['sell_price']} ({simbolo}/kg)", value=2.10 * cambio, format="%.2f") / cambio
c_en = st.sidebar.number_input(f"{t['energy_cost']} ({simbolo}/kWh)", value=0.22 * cambio, format="%.2f") / cambio
h_an = st.sidebar.number_input(t['hours'], value=8000)
tol_m = st.sidebar.slider(t['market_tol'], 1.0, 10.0, 6.0)

# --- INPUT COLONNE ---
st.header(t['header_comp'])
col_a, col_b = st.columns(2)

with col_a:
    st.subheader(t['line_a'])
    ca_val = st.number_input(f"{t['capex']} A ({simbolo})", value=int(1500000 * cambio), step=10000, key="a1")
    ca = ca_val / cambio
    pa = st.number_input(f"{t['output']} A (kg/h)", value=400, key="a2")
    csa = st.number_input(f"{t['cons']} A (kWh/kg)", value=0.40, key="a3")
    sa = st.number_input(f"{t['precision']} A (±%)", value=4.5, key="a4")
    ma = st.number_input(f"{t['maint']} A (%)", value=3.5, key="a5")
    oa = st.number_input(f"{t['oee']} A (%)", value=80.0, key="a6")
    scra = st.number_input(f"{t['scrap']} A (%)", value=3.0, key="a7")

with col_b:
    st.subheader(t['line_b'])
    cb_val = st.number_input(f"{t['capex']} B ({simbolo})", value=int(2000000 * cambio), step=10000, key="b1")
    cb = cb_val / cambio
    pb = st.number_input(f"{t['output']} B (kg/h)", value=440, key="b2")
    csb = st.number_input(f"{t['cons']} B (kWh/kg)", value=0.35, key="b3")
    sb = st.number_input(f"{t['precision']} B (±%)", value=1.5, key="b4")
    mb = st.number_input(f"{t['maint']} B (%)", value=2.0, key="b5")
    ob = st.number_input(f"{t['oee']} B (%)", value=85.0, key="b6")
    scrb = st.number_input(f"{t['scrap']} B (%)", value=1.5, key="b7")

# --- CALCOLI ---
pra, prb = pa * h_an * (oa/100), pb * h_an * (ob/100)
neta, netb = pra * (1 - scra/100), prb * (1 - scrb/100)
mata, matb = pra * c_pe, prb * c_pe * (1 - (tol_m - sb)/100)
enea, eneb = pra * csa * c_en, prb * csb * c_en
mnta, mntb = ca * (ma/100), cb * (mb/100)
opexa, opexb = mata + enea + mnta, matb + eneb + mntb
ckga, ckgb = (opexa + (ca/10)) / neta, (opexb + (cb/10)) / netb
marga, margb = (neta * p_ve) - opexa, (netb * p_ve) - opexb
dmarg = margb - marga
p5y = (dmarg * 5) - (cb - ca)
pbk = (cb - ca) / dmarg if dmarg > 0 else 0

# --- TABELLA COMPARATIVA ---
st.markdown("---")
st.subheader(t['tech_comp'])
data = {
    "Parameter": [t['capex'], t['output'], t['oee'], t['scrap'], t['cons'], t['cost_kg'], t['extra_margin']],
    t['line_a']: [f"{simbolo} {ca*cambio:,.0f}", f"{pa} kg/h", f"{oa}%", f"{scra}%", f"{csa} kWh/kg", f"{simbolo} {ckga*cambio:.3f}", f"{simbolo} {marga*cambio:,.0f}"],
    t['line_b']: [f"{simbolo} {cb*cambio:,.0f}", f"{pb} kg/h", f"{ob}%", f"{scrb}%", f"{csb} kWh/kg", f"{simbolo} {ckgb*cambio:.3f}", f"{simbolo} {margb*cambio:,.0f}"],
    t['diff_col']: [f"🔴 +{simbolo} {(cb-ca)*cambio:,.0f}", f"📈 +{pb-pa} kg/h", f"✅ +{ob-oa}%", f"📉 {scrb-scra}%", f"📉 {csb-csa:.2f} kWh/kg", f"✅ -{simbolo} {(ckga-ckgb)*cambio:.3f}", f"🔥 +{simbolo} {dmarg*cambio:,.0f}"]
}
st.table(pd.DataFrame(data))

# --- RISULTATI ROI ---
st.title(t['res_title'])
if dmarg > 0:
    c1, c2, c3 = st.columns(3)
    c1.metric(t['extra_margin'], f"{simbolo} {dmarg*cambio:,.0f}")
    c2.metric(t['payback'], f"{pbk:.1f} Yrs")
    c3.metric(t['profit_5y'], f"{simbolo} {p5y*cambio:,.0f}")
    st.info(t['info_msg'].format(simbolo, (ckga - ckgb)*cambio, simbolo, p5y*cambio))

    # --- GENERAZIONE REPORT TESTUALE ---
    # Logica multilingua per il testo del report
    report_titles = {
        "English": ["FINANCIAL OVERVIEW", "PERFORMANCE DRIVERS", "CONCLUSION", "Line B Premium"],
        "Italiano": ["PANORAMICA FINANZIARIA", "FATTORI DI PERFORMANCE", "CONCLUSIONE", "Linea B Premium"],
        "Deutsch": ["FINANZIELLE ÜBERSICHT", "LEISTUNGSFAKTOREN", "FAZIT", "Linie B Premium"],
        "Español": ["RESUMEN FINANCIERO", "FACTORES DE RENDIMIENTO", "CONCLUSIÓN", "Línea B Premium"]
    }
    rt = report_titles[lingua]

    report_text = f"""
============================================================
STRATEGIC ROI ANALYSIS REPORT ({val_code}) - {lingua.upper()}
============================================================

1. {rt[0]} ({simbolo})
------------------------------------------------------------
- Extra Investment (B-A): {simbolo} {(cb-ca)*cambio:,.0f}
- Extra Annual Margin:    {simbolo} {dmarg*cambio:,.0f}
- Payback Period:         {pbk:.1f} Years
- 5-Year Extra Profit:    {simbolo} {p5y*cambio:,.0f}

2. {rt[1]}: WHY {rt[3]}?
------------------------------------------------------------
- RAW MATERIAL SAVINGS: 2σ precision ({sb}%) vs ({sa}%).
- OPERATIONAL EXCELLENCE: OEE {ob}% vs {oa}%.
- WASTE REDUCTION: Scrap {scrb}% vs {scra}%.
- PRODUCTION COST PER KG: {simbolo} {ckgb*cambio:.3f}

3. {rt[2]}
------------------------------------------------------------
The higher initial investment is justified by lower 
operational costs and superior annual profitability.
============================================================
"""
    st.download_button(t['download_btn'], report_text, file_name=f"Strategic_Report_{val_code}_{lingua}.txt")

    # Grafico Cash Flow
    yrs = list(range(11))
    fa = [(-ca + (marga * i)) * cambio for i in yrs]
    fb = [(-cb + (margb * i)) * cambio for i in yrs]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=yrs, y=fa, name=t['line_a'], line=dict(color='gray', dash='dot')))
    fig.add_trace(go.Scatter(x=yrs, y=fb, name=t['line_b'], line=dict(color='#00CC96', width=4)))
    fig.add_hline(y=0, line_color="black")
    fig.update_layout(title=f"Cumulative Cash Flow ({val_code})", xaxis_title="Years", yaxis_title=simbolo)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("Negative ROI - Check inputs.")
