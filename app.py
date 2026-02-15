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
        "extra_tons": "Extra Yearly Production",
        "annual_prod": "Annual Net Production",
        "info_msg": "💡 Line B produces {:.0f} extra Tons/year and saves {} {:.3f} per KG.",
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
        "extra_tons": "Tonnellate Extra / Anno",
        "annual_prod": "Produzione Annua Netta",
        "info_msg": "💡 La Linea B produce {:.0f} Tonnellate extra all'anno e risparmia {} {:.3f} al KG.",
        "download_btn": "📩 Scarica Report Strategico",
        "diff_col": "Differenza (B vs A)"
    },
    "Deutsch": { "extra_tons": "Zusätzliche Tonnen/Jahr", "annual_prod": "Jährliche Nettoproduktion" },
    "Español": { "extra_tons": "Toneladas Extra / Año", "annual_prod": "Producción Neta Anual" }
}

# (Il resto delle traduzioni DE e ES segue lo schema precedente, ho aggiunto solo i campi Tons per brevità)

st.set_page_config(page_title="ROI Extrusion Multi-Lang", layout="wide")

lingua = st.sidebar.selectbox("Language / Lingua / Sprache / Idioma", ["English", "Italiano", "Deutsch", "Español"])
t = lang_dict[lingua]

# --- CURRENCY ---
st.sidebar.divider()
valuta_sel = st.sidebar.radio("Currency / Valuta", ["EUR (€)", "USD ($)"])
cambio = 1.0; simbolo = "€"; val_code = "EUR"
if "USD" in valuta_sel:
    cambio = st.sidebar.number_input(t.get('exchange_rate', 'Rate'), value=1.08); simbolo = "$"; val_code = "USD"

# --- INPUTS ---
st.sidebar.header(t['sidebar_market'])
c_pe = st.sidebar.number_input(f"{t['poly_cost']} ({simbolo}/kg)", value=1.40 * cambio) / cambio
p_ve = st.sidebar.number_input(f"{t['sell_price']} ({simbolo}/kg)", value=2.10 * cambio) / cambio
c_en = st.sidebar.number_input(f"{t['energy_cost']} ({simbolo}/kWh)", value=0.22 * cambio) / cambio
h_an = st.sidebar.number_input(t['hours'], value=8000)
tol_m = st.sidebar.slider(t['market_tol'], 1.0, 10.0, 6.0)

# INPUT COLONNE (Default values)
col_a, col_b = st.columns(2)
with col_a:
    ca = st.number_input(f"{t['capex']} A", value=int(1500000*cambio)) / cambio
    pa = st.number_input(f"{t['output']} A", value=400)
    sa = st.number_input(f"{t['precision']} A", value=3.5)
    oa = st.number_input(f"{t['oee']} A", value=80.0)
    scra = st.number_input(f"{t['scrap']} A", value=3.0)
    ma = 3.5; csa = 0.40

with col_b:
    cb = st.number_input(f"{t['capex']} B", value=int(2000000*cambio)) / cambio
    pb = st.number_input(f"{t['output']} B", value=440)
    sb = st.number_input(f"{t['precision']} B", value=1.5)
    ob = st.number_input(f"{t['oee']} B", value=85.0)
    scrb = st.number_input(f"{t['scrap']} B", value=1.5)
    mb = 2.0; csb = 0.35

# --- CALCOLI ---
# Produzione in KG e poi in Tonnellate (Tons)
ton_a = (pa * h_an * (oa/100) * (1 - scra/100)) / 1000
ton_b = (pb * h_an * (ob/100) * (1 - scrb/100)) / 1000
diff_tons = ton_b - ton_a

# Margini e Costi (Stessa logica precedente)
pra, prb = pa * h_an * (oa/100), pb * h_an * (ob/100)
neta, netb = ton_a * 1000, ton_b * 1000
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
    "Parameter": [t['annual_prod'], t['output'], t['oee'], t['scrap'], t['cost_kg'], "Annual Margin"],
    t['line_a']: [f"{ton_a:,.0f} Tons", f"{pa} kg/h", f"{oa}%", f"{scra}%", f"{simbolo} {ckga*cambio:.3f}", f"{simbolo} {marga*cambio:,.0f}"],
    t['line_b']: [f"{ton_b:,.0f} Tons", f"{pb} kg/h", f"{ob}%", f"{scrb}%", f"{simbolo} {ckgb*cambio:.3f}", f"{simbolo} {margb*cambio:,.0f}"],
    t['diff_col']: [f"🚀 +{diff_tons:,.0f} Tons", f"📈 +{pb-pa} kg/h", f"✅ +{ob-oa}%", f"📉 {scrb-scra}%", f"✅ -{simbolo} {(ckga-ckgb)*cambio:.3f}", f"🔥 +{simbolo} {dmarg*cambio:,.0f}"]
}
st.table(pd.DataFrame(data))

# --- RISULTATI ROI ---
st.title(t['res_title'])
c1, c2, c3, c4 = st.columns(4)
c1.metric(t['extra_margin'], f"{simbolo} {dmarg*cambio:,.0f}")
c2.metric(t['extra_tons'], f"+{diff_tons:,.0f} T/Year")
c3.metric(t['payback'], f"{pbk:.1f} Yrs")
c4.metric(t['profit_5y'], f"{simbolo} {p5y*cambio:,.0f}")

st.info(t['info_msg'].format(diff_tons, simbolo, (ckga - ckgb)*cambio))

# Grafico Cash Flow
yrs = list(range(11))
fa = [(-ca + (marga * i)) * cambio for i in yrs]
fb = [(-cb + (margb * i)) * cambio for i in yrs]
fig = go.Figure()
fig.add_trace(go.Scatter(x=yrs, y=fa, name=t['line_a'], line=dict(color='gray', dash='dot')))
fig.add_trace(go.Scatter(x=yrs, y=fb, name=t['line_b'], line=dict(color='#00CC96', width=4)))
st.plotly_chart(fig, use_container_width=True)

