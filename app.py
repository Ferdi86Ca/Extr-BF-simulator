import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from fpdf import FPDF

# 1. DIZIONARIO TRADUZIONI (Completo: EN, IT, DE, ES)
lang_dict = {
    "English": {
        "title": "ROI Extrusion Multi-Lang",
        "line_a": "Line A (Standard)",
        "line_p": "Premium Line",
        "res_title": "ROI Analysis Results",
        "extra_tons": "Extra Tons/Year",
        "payback": "Payback (Years)",
        "profit_5y": "5y Extra Profit",
        "download_pdf": "Download PDF Report"
    },
    "Italiano": {
        "title": "ROI Extrusion Multi-Lang",
        "line_a": "Linea A (Standard)",
        "line_p": "Linea Premium",
        "res_title": "Risultati Analisi ROI",
        "extra_tons": "Tonnellate Extra/Anno",
        "payback": "Pareggio (Anni)",
        "profit_5y": "Extra Profitto (5 anni)",
        "download_pdf": "Scarica Report PDF"
    },
    "Deutsch": {
        "title": "ROI Extrusion Multi-Lang",
        "line_a": "Linie A (Standard)",
        "line_p": "Premium-Linie",
        "res_title": "ROI-Analyseergebnisse",
        "extra_tons": "Zusatzliche Tonnen/Jahr",
        "payback": "Amortisation (Jahre)",
        "profit_5y": "Extra Profit (5 J.)",
        "download_pdf": "PDF-Bericht herunterladen"
    },
    "Español": {
        "title": "ROI Extrusion Multi-Lang",
        "line_a": "Linea A (Estandar)",
        "line_p": "Linea Premium",
        "res_title": "Resultados del Analisis ROI",
        "extra_tons": "Toneladas Extra/Ano",
        "payback": "Retorno (Anos)",
        "profit_5y": "Beneficio Extra (5a)",
        "download_pdf": "Descargar Reporte PDF"
    }
}

st.set_page_config(page_title="ROI Extrusion", layout="wide")

# --- SIDEBAR: LINGUA E VALUTA ---
st.sidebar.header("Settings")
sel_lang = st.sidebar.selectbox("Language", ["English", "Italiano", "Deutsch", "Español"])
t = lang_dict[sel_lang]

valuta = st.sidebar.radio("Currency", ["EUR", "USD"])
cambio = 1.08 if valuta == "USD" else 1.0
simbolo = "$" if valuta == "USD" else "EUR"

# --- INPUT PARAMETRI DI MERCATO ---
st.sidebar.divider()
st.sidebar.subheader("Market Data")
c_poly = st.sidebar.number_input(f"Polymer Cost ({simbolo}/kg)", value=1.40 * cambio) / cambio
p_sell = st.sidebar.number_input(f"Selling Price ({simbolo}/kg)", value=2.10 * cambio) / cambio
c_energy = st.sidebar.number_input(f"Energy Cost ({simbolo}/kWh)", value=0.22 * cambio) / cambio
hours = st.sidebar.number_input("Working Hours/Year", value=8000)
tolerance = st.sidebar.slider("Market Tolerance (±%)", 1.0, 10.0, 6.0)

# --- CORPO PRINCIPALE: COMPARAZIONE ---
st.title(t['title'])
col1, col2 = st.columns(2)

with col1:
    st.subheader(t['line_a'])
    ca = st.number_input("Investment A", value=1500000, step=50000)
    pa = st.number_input("Output A (kg/h)", value=400)
    oa = st.number_input("OEE A (%)", value=75.0)
    sa = st.number_input("2-Sigma Precision A (%)", value=4.5)
    scra = st.number_input("Scrap Rate A (%)", value=4.0)
    ma, csa = 3.5, 0.40 # Maint % e Consumo kWh/kg

with col2:
    st.subheader(t['line_p'])
    cp = st.number_input("Investment Premium", value=2000000, step=50000)
    pp = st.number_input("Output Premium (kg/h)", value=440)
    op = st.number_input("OEE Premium (%)", value=85.0)
    sp = st.number_input("2-Sigma Precision Premium (%)", value=1.5)
    scrp = st.number_input("Scrap Rate Premium (%)", value=1.5)
    mp, csp = 2.0, 0.35

# --- LOGICA CALCOLI ---
# Produzione
ton_a = (pa * hours * (oa/100) * (1 - scra/100)) / 1000
ton_p = (pp * hours * (op/100) * (1 - scrp/100)) / 1000
diff_tons = ton_p - ton_a

# Costi Operativi (OPEX)
pra, prp = pa * hours * (oa/100), pp * hours * (op/100)
cost_mat_a = pra * c_poly
cost_mat_p = prp * c_poly * (1 - (tolerance - sp)/100) # Risparmio grazie a precisione
cost_ene_a = pra * csa * c_energy
cost_ene_p = prp * csp * c_energy
cost_maint_a = ca * (ma/100)
cost_maint_p = cp * (mp/100)

opex_a = cost_mat_a + cost_ene_a + cost_maint_a
opex_p = cost_mat_p + cost_ene_p + cost_maint_p

# Margini e ROI
marga = (ton_a * 1000 * p_sell) - opex_a
margp = (ton_p * 1000 * p_sell) - opex_p
dmarg = margp - marga
pbk = (cp - ca) / dmarg if dmarg > 0 else 0
p5y = (dmarg * 5) - (cp - ca)
saving_kg = (opex_a/ (ton_a*1000)) - (opex_p/ (ton_p*1000)) if ton_a > 0 else 0

# --- VISUALIZZAZIONE RISULTATI ---
st.divider()
st.header(t['res_title'])
k1, k2, k3, k4 = st.columns(4)
k1.metric("Extra Margin/Year", f"{simbolo} {dmarg*cambio:,.0f}")
k2.metric(t['extra_tons'], f"+{diff_tons:,.0f} T")
k3.metric(t['payback'], f"{pbk:.1f} Yrs")
k4.metric(t['profit_5y'], f"{simbolo} {p5y*cambio:,.0f}")

# --- TABELLA TECNICA ---
st.subheader("Technical Details")
df_data = {
    "Metric": ["Annual Production", "Scrap Rate", "OEE Efficiency", "Specific Consumption"],
    t['line_a']: [f"{ton_a:,.0f} Tons", f"{scra}%", f"{oa}%", f"{csa} kWh/kg"],
    t['line_p']: [f"{ton_p:,.0f} Tons", f"{scrp}%", f"{op}%", f"{csp} kWh/kg"],
    "Improvement": [f"+{diff_tons:,.0f} Tons", f"-{scra-scrp}%", f"+{op-oa}%", f"-{csa-csp:.2f}"]
}
st.table(pd.DataFrame(df_data))

# --- GENERAZIONE PDF ---
def make_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(190, 10, "ROI ANALYSIS: STANDARD VS PREMIUM", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.cell(100, 10, f"Currency: {valuta}")
    pdf.cell(100, 10, f"Payback: {pbk:.1f} Years", ln=True)
    pdf.cell(100, 10, f"Extra Profit 5y: {simbolo} {p5y*cambio:,.0f}")
    pdf.cell(100, 10, f"Extra Tons/Year: {diff_tons:,.0f} T", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "Strategic Conclusion", ln=True)
    pdf.set_font("Arial", "", 11)
    msg = f"The Premium Line reduces cost per kg and increases production by {diff_tons:,.0f} tons."
    pdf.multi_cell(180, 8, msg)
    return pdf.output(dest='S').encode('latin-1', 'replace')

if st.button(t['download_pdf']):
    pdf_out = make_pdf()
    st.download_button("Click to Download", data=pdf_out, file_name="ROI_Report.pdf", mime="application/pdf")
