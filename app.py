import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from fpdf import FPDF

# 1. DIZIONARIO TRADUZIONI COMPLETO (Correzione KeyError)
lang_dict = {
    "English": {
        "title": "ROI Extrusion",
        "line_a": "Standard Line",
        "line_b": "Premium Line",
        "res_title": "ROI Analysis Results",
        "tech_comp": "Comparative Performance & Indicators",
        "download_pdf": "Download Rich Strategic Report (PDF)",
        "extra_tons": "Extra Tons/Year",
        "payback": "Payback (Years)",
        "profit_5y": "5y Extra Profit",
        "cost_kg": "Prod. Cost per KG",
        "annual_prod": "Annual Net Production",
        "margin_yr": "Annual Margin",
        "exchange_rate": "Exchange Rate (1€ = X $)"
    },
    "Italiano": {
        "title": "ROI Extrusion",
        "line_a": "Linea Standard",
        "line_b": "Linea Premium",
        "res_title": "Risultati Analisi ROI",
        "tech_comp": "Comparazione Performance e Indicatori",
        "download_pdf": "Scarica Report Strategico Avanzato (PDF)",
        "extra_tons": "Tonnellate Extra/Anno",
        "payback": "Pareggio (Anni)",
        "profit_5y": "Extra Profitto (5 anni)",
        "cost_kg": "Costo al KG",
        "annual_prod": "Produzione Annua Netta",
        "margin_yr": "Margine Annuo",
        "exchange_rate": "Tasso di Cambio (1€ = X $)"
    },
    "Deutsch": {
        "title": "ROI Extrusion",
        "line_a": "Standard-Linie",
        "line_b": "Premium-Linie",
        "res_title": "ROI-Analyseergebnisse",
        "tech_comp": "Leistungsvergleich & Indikatoren",
        "download_pdf": "Strategischen Bericht herunterladen (PDF)",
        "extra_tons": "Zusätzliche Tonnen/Jahr",
        "payback": "Amortisation (Jahre)",
        "profit_5y": "Extra-Profit (5 J.)",
        "cost_kg": "Prod.-Kosten pro KG",
        "annual_prod": "Jährliche Nettoproduktion",
        "margin_yr": "Jährliche Marge",
        "exchange_rate": "Wechselkurs (1€ = X $)"
    },
    "Español": {
        "title": "ROI Extrusion",
        "line_a": "Línea Estándar",
        "line_b": "Línea Premium",
        "res_title": "Resultados del Análisis ROI",
        "tech_comp": "Comparativa de Rendimiento e Indicadores",
        "download_pdf": "Descargar Informe Estratégico (PDF)",
        "extra_tons": "Toneladas Extra/Año",
        "payback": "Retorno (Años)",
        "profit_5y": "Extra Beneficio (5a)",
        "cost_kg": "Costo de Prod. por KG",
        "annual_prod": "Producción Neta Anual",
        "margin_yr": "Margen Anual",
        "exchange_rate": "Tipo de Cambio (1€ = X $)"
    }
}

st.set_page_config(page_title="ROI Extrusion", layout="wide")

# Selezione Lingua (Ordine richiesto)
lingua = st.sidebar.selectbox("Language / Lingua / Sprache / Idioma", ["English", "Italiano", "Deutsch", "Español"])
t = lang_dict[lingua]

st.title(t['title'])

# --- SIDEBAR CURRENCY & MARKET ---
valuta_sel = st.sidebar.radio("Currency / Valuta", ["EUR", "USD"])
cambio = 1.0; simbolo = "EUR"
if valuta_sel == "USD":
    cambio = st.sidebar.number_input(t['exchange_rate'], value=1.08)
    simbolo = "USD"

st.sidebar.divider()
c_poly = st.sidebar.number_input(f"Polymer Cost ({simbolo}/kg)", value=1.40 * cambio) / cambio
p_sell = st.sidebar.number_input(f"Selling Price ({simbolo}/kg)", value=2.10 * cambio) / cambio
c_ene = st.sidebar.number_input(f"Energy Cost ({simbolo}/kWh)", value=0.22 * cambio) / cambio
h_an = st.sidebar.number_input("Hours/Year", value=8000)
tol_m = st.sidebar.slider("Market Tol. (±%)", 1.0, 10.0, 6.0)

# --- INPUT COMPARAZIONE ---
col_a, col_p = st.columns(2)
with col_a:
    st.subheader(f"📊 {t['line_a']}")
    ca = st.number_input("CAPEX Standard", value=1500000, key="ca_in")
    pa = st.number_input("Output (kg/h) Standard", value=400, key="pa_in")
    oa = st.number_input("OEE (%) Standard", value=75.0, key="oa_in")
    sa = st.number_input("2-Sigma (%) Standard", value=4.5, key="sa_in")
    scra = st.number_input("Scrap (%) Standard", value=4.0, key="scra_in")
    ma, csa = 3.5, 0.40

with col_p:
    st.subheader(f"🚀 {t['line_b']}")
    cp = st.number_input("CAPEX Premium", value=2000000, key="cp_in")
    pp = st.number_input("Output (kg/h) Premium", value=440, key="pp_in")
    op = st.number_input("OEE (%) Premium", value=85.0, key="op_in")
    sp = st.number_input("2-Sigma (%) Premium", value=1.5, key="sp_in")
    scrp = st.number_input("Scrap (%) Premium", value=1.5, key="scrp_in")
    mp, csp = 2.0, 0.35

# --- CALCOLI ---
ton_a = (pa * h_an * (oa/100) * (1 - scra/100)) / 1000
ton_p = (pp * h_an * (op/100) * (1 - scrp/100)) / 1000
diff_tons = ton_p - ton_a

opexa = (pa*h_an*(oa/100)*c_poly) + (pa*h_an*(oa/100)*csa*c_ene) + (ca*ma/100)
opexp = (pp*h_an*(op/100)*c_poly*(1-(tol_m-sp)/100)) + (pp*h_an*(op/100)*csp*c_ene) + (cp*mp/100)

ckga = (opexa + (ca/10)) / (ton_a*1000) if ton_a > 0 else 0
ckgp = (opexp + (cp/10)) / (ton_p*1000) if ton_p > 0 else 0
marga = (ton_a*1000*p_sell) - opexa
margp = (ton_p*1000*p_sell) - opexp
dmarg = margp - marga
pbk = (cp - ca) / dmarg if dmarg > 0 else 0
p5y = (dmarg * 5) - (cp - ca)

# --- VISUALIZZAZIONE TABELLA ---
st.subheader(t['tech_comp'])
df_comp = pd.DataFrame({
    "Metric": [t['annual_prod'], "OEE", "Scrap", t['cost_kg'], t['margin_yr']],
    t['line_a']: [f"{ton_a:,.0f} T", f"{oa}%", f"{scra}%", f"{simbolo} {ckga*cambio:.3f}", f"{simbolo} {marga*cambio:,.0f}"],
    t['line_b']: [f"{ton_p:,.0f} T", f"{op}%", f"{scrp}%", f"{simbolo} {ckgp*cambio:.3f}", f"{simbolo} {margp*cambio:,.0f}"],
    "Diff": [f"+{diff_tons:,.0f} T", f"+{op-oa}%", f"-{scra-scrp}%", f"-{simbolo} {(ckga-ckgp)*cambio:.3f}", f"+{simbolo} {dmarg*cambio:,.0f}"]
})
st.table(df_comp)

# --- KPI ---
st.header(t['res_title'])
k1, k2, k3, k4 = st.columns(4)
k1.metric(t['margin_yr'] + " Extra", f"{simbolo} {dmarg*cambio:,.0f}")
k2.metric(t['extra_tons'], f"+{diff_tons:,.0f} T")
k3.metric(t['payback'], f"{pbk:.1f} Yrs")
k4.metric(t['profit_5y'], f"{simbolo} {p5y*cambio:,.0f}")

# --- GRAFICO ---
yrs = list(range(11))
fa = [(-ca + (marga * i)) * cambio for i in yrs]
fp = [(-cp + (margp * i)) * cambio for i in yrs]
fig = go.Figure()
fig.add_trace(go.Scatter(x=yrs, y=fa, name=t['line_a'], line=dict(color='gray', dash='dot')))
fig.add_trace(go.Scatter(x=yrs, y=fp, name=t['line_b'], line=dict(color='#00CC96', width=4)))
fig.add_hline(y=0, line_color="black")
fig.update_layout(title="Cumulative Cash Flow Analysis", xaxis_title="Years", yaxis_title=simbolo)
st.plotly_chart(fig, use_container_width=True)

# --- PDF ---
def create_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(190, 10, "ROI EXTRUSION - STRATEGIC REPORT", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "1. FINANCIAL OVERVIEW (" + simbolo + ")", ln=True, fill=False)
    pdf.set_font("Arial", "", 10)
    pdf.cell(95, 10, f"Payback: {pbk:.1f} Years", 1)
    pdf.cell(95, 10, f"5y Extra Profit: {simbolo} {p5y*cambio:,.0f}", 1, 1)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "2. TECHNICAL COMPARISON", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(60, 10, "Metric", 1); pdf.cell(65, 10, t['line_a'], 1); pdf.cell(65, 10, t['line_b'], 1, 1)
    pdf.cell(60, 10, "Net Production", 1); pdf.cell(65, 10, f"{ton_a:,.0f} T", 1); pdf.cell(65, 10, f"{ton_p:,.0f} T", 1, 1)
    pdf.cell(60, 10, "Scrap Rate", 1); pdf.cell(65, 10, f"{scra}%", 1); pdf.cell(65, 10, f"{scrp}%", 1, 1)
    pdf.ln(10)
    pdf.multi_cell(190, 8, f"Conclusion: The Premium Line reduces cost per kg and adds {diff_tons:,.0f} tons/year of sellable product.")
    return pdf.output(dest='S').encode('latin-1', 'replace')

st.divider()
if st.button(t['download_pdf']):
    st.download_button("Download Now", data=create_pdf(), file_name="ROI_Extrusion_Report.pdf", mime="application/pdf")
