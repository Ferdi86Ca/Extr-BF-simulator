import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from fpdf import FPDF

# 1. TRADUZIONI COMPLETE
lang_dict = {
    "English": {
        "title": "ROI Extrusion Multi-Lang",
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
        "line_b": "Line Premium",
        "capex": "Investment",
        "output": "Output (kg/h)",
        "cons": "Consumption (kWh/kg)",
        "precision": "2σ Precision (±%)",
        "maint": "Maint. (%)",
        "oee": "OEE Efficiency (%)",
        "scrap": "Scrap Rate (%)",
        "res_title": "🏁 ROI Analysis Results",
        "tech_comp": "📊 Comparative Performance & Differences",
        "extra_margin": "Extra Annual Margin",
        "payback": "Payback (Years)",
        "cost_kg": "Prod. Cost per KG",
        "profit_5y": "Extra Profit (5y)",
        "extra_tons": "Extra Yearly Production",
        "annual_prod": "Annual Net Production",
        "info_msg": "💡 Premium Line produces {:.0f} extra Tons/year and saves {} {:.3f} per KG.",
        "download_pdf": "📩 Download PDF Report",
        "diff_col": "Difference (Premium vs A)"
    },
    "Italiano": {
        "title": "ROI Extrusion Multi-Lang",
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
        "line_b": "Linea Premium",
        "capex": "Investimento",
        "output": "Portata (kg/h)",
        "cons": "Consumo (kWh/kg)",
        "precision": "Precisione 2σ (±%)",
        "maint": "Manutenzione (%)",
        "oee": "OEE - Efficienza (%)",
        "scrap": "Percentuale Scarto (%)",
        "res_title": "🏁 Risultati Analisi ROI",
        "tech_comp": "📊 Comparazione Performance e Differenze",
        "extra_margin": "Extra Margine Annuo",
        "payback": "Pareggio (Anni)",
        "cost_kg": "Costo al KG",
        "profit_5y": "Extra Profitto (5 anni)",
        "extra_tons": "Tonnellate Extra / Anno",
        "annual_prod": "Produzione Annua Netta",
        "info_msg": "💡 La Linea Premium produce {:.0f} Tonnellate extra all'anno e risparmia {} {:.3f} al KG.",
        "download_pdf": "📩 Scarica Report PDF",
        "diff_col": "Differenza (Premium vs A)"
    },
    "Deutsch": { "title": "ROI Extrusion Multi-Lang", "line_a": "Linie A", "line_b": "Premium-Linie", "extra_tons": "Zusatzliche T/Jahr" },
    "Español": { "title": "ROI Extrusion Multi-Lang", "line_a": "Linea A", "line_b": "Linea Premium", "extra_tons": "Toneladas Extra/Ano" }
}

st.set_page_config(page_title="ROI Extrusion Multi-Lang", layout="wide")

# --- SELETTORE LINGUA ---
lingua = st.sidebar.selectbox("Language / Lingua", ["English", "Italiano", "Deutsch", "Español"])
t = lang_dict[lingua]

# --- CURRENCY ---
st.sidebar.divider()
valuta_sel = st.sidebar.radio(t.get('currency_settings', 'Currency'), ["EUR", "USD"])
cambio = 1.0; simbolo = "EUR"; val_code = "EUR"
if valuta_sel == "USD":
    cambio = st.sidebar.number_input(t.get('exchange_rate', 'Rate'), value=1.08)
    simbolo = "USD"; val_code = "USD"

# --- INPUT MERCATO ---
st.sidebar.header(t['sidebar_market'])
c_poly = st.sidebar.number_input(f"{t['poly_cost']} ({simbolo})", value=1.40 * cambio) / cambio
p_sell = st.sidebar.number_input(f"{t['sell_price']} ({simbolo})", value=2.10 * cambio) / cambio
c_ene = st.sidebar.number_input(f"{t['energy_cost']} ({simbolo})", value=0.22 * cambio) / cambio
h_an = st.sidebar.number_input(t['hours'], value=8000)
tol_m = st.sidebar.slider(t['market_tol'], 1.0, 10.0, 6.0)

# --- COMPARISON ---
st.title(t['title'])
col_a, col_p = st.columns(2)

with col_a:
    st.subheader(t['line_a'])
    ca = st.number_input(f"{t['capex']} A", value=1500000)
    pa = st.number_input(f"{t['output']} A", value=400)
    oa = st.number_input(f"{t['oee']} A", value=75.0)
    sa = st.number_input(f"{t['precision']} A", value=4.5)
    scra = st.number_input(f"{t['scrap']} A", value=4.0)
    ma, csa = 3.5, 0.40

with col_p:
    st.subheader(t['line_b'])
    cp = st.number_input(f"{t['capex']} Premium", value=2000000)
    pp = st.number_input(f"{t['output']} Premium", value=440)
    op = st.number_input(f"{t['oee']} Premium", value=85.0)
    sp = st.number_input(f"{t['precision']} Premium", value=1.5)
    scrp = st.number_input(f"{t['scrap']} Premium", value=1.5)
    mp, csp = 2.0, 0.35

# --- CALCOLI ---
ton_a = (pa * h_an * (oa/100) * (1 - scra/100)) / 1000
ton_p = (pp * h_an * (op/100) * (1 - scrp/100)) / 1000
diff_tons = ton_p - ton_a

# OPEX & MARGINI
opexa = (pa*h_an*(oa/100)*c_poly) + (pa*h_an*(oa/100)*csa*c_ene) + (ca*ma/100)
opexp = (pp*h_an*(op/100)*c_poly*(1-(tol_m-sp)/100)) + (pp*h_an*(op/100)*csp*c_ene) + (cp*mp/100)

ckga, ckgp = (opexa + (ca/10)) / (ton_a*1000), (opexp + (cp/10)) / (ton_p*1000)
marga, margp = (ton_a*1000*p_sell) - opexa, (ton_p*1000*p_sell) - opexp
dmarg = margp - marga
pbk = (cp - ca) / dmarg if dmarg > 0 else 0
p5y = (dmarg * 5) - (cp - ca)

# --- TABELLA COMPARATIVA ---
st.subheader(t['tech_comp'])
data = {
    "Parameter": [t['annual_prod'], t['oee'], t['scrap'], t['cost_kg'], "Annual Margin"],
    t['line_a']: [f"{ton_a:,.0f} T", f"{oa}%", f"{scra}%", f"{simbolo} {ckga*cambio:.3f}", f"{simbolo} {marga*cambio:,.0f}"],
    t['line_b']: [f"{ton_p:,.0f} T", f"{op}%", f"{scrp}%", f"{simbolo} {ckgp*cambio:.3f}", f"{simbolo} {margp*cambio:,.0f}"],
    t['diff_col']: [f"📈 +{diff_tons:,.0f} T", f"✅ +{op-oa}%", f"📉 {scrp-scra}%", f"✅ -{simbolo} {(ckga-ckgp)*cambio:.3f}", f"🔥 +{simbolo} {dmarg*cambio:,.0f}"]
}
st.table(pd.DataFrame(data))

# --- KPI & GRAFICO ---
st.header(t['res_title'])
k1, k2, k3, k4 = st.columns(4)
k1.metric(t['extra_margin'], f"{simbolo} {dmarg*cambio:,.0f}")
k2.metric(t['extra_tons'], f"+{diff_tons:,.0f} T")
k3.metric(t['payback'], f"{pbk:.1f} Yrs")
k4.metric(t['profit_5y'], f"{simbolo} {p5y*cambio:,.0f}")

# GRAFICO PAYBACK
yrs = list(range(11))
fa = [(-ca + (marga * i)) * cambio for i in yrs]
fp = [(-cp + (margp * i)) * cambio for i in yrs]
fig = go.Figure()
fig.add_trace(go.Scatter(x=yrs, y=fa, name=t['line_a'], line=dict(color='gray', dash='dot')))
fig.add_trace(go.Scatter(x=yrs, y=fp, name=t['line_b'], line=dict(color='#00CC96', width=4)))
fig.add_hline(y=0, line_color="black")
fig.update_layout(title="Payback Strategy: Cumulative Cash Flow", xaxis_title="Years", yaxis_title=simbolo)
st.plotly_chart(fig, use_container_width=True)

# --- PDF GENERATOR (Safe Mode) ---
def make_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(190, 10, "STRATEGIC ROI REPORT", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.cell(100, 10, f"Payback Period: {pbk:.1f} Years")
    pdf.cell(100, 10, f"5-Year Extra Profit: {simbolo} {p5y*cambio:,.0f}", ln=True)
    pdf.cell(100, 10, f"Extra Production: {diff_tons:,.0f} Tons/Year")
    pdf.ln(10)
    pdf.multi_cell(180, 8, f"Conclusion: The Premium Line generates {simbolo} {dmarg*cambio:,.0f} extra margin per year by reducing scrap and increasing OEE.")
    return pdf.output(dest='S').encode('latin-1', 'replace')

if st.button(t['download_pdf']):
    st.download_button("Save Report PDF", data=make_pdf(), file_name="ROI_Premium.pdf", mime="application/pdf")
