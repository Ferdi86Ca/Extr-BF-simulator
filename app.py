import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from fpdf import FPDF
import tempfile
import os

# 1. DIZIONARIO TRADUZIONI COMPLETO
lang_dict = {
    "English": {
        "title": "ROI Extrusion Strategic Advisor",
        "tech_comp": "📊 Technical & Operational Comparison",
        "fin_comp": "💰 Asset Performance & Financial Yield",
        "res_title": "🏁 ROI Analysis Results",
        "download_pdf": "📩 Download FULL Strategic Report (PDF)",
        "annual_prod": "Annual Net Production",
        "margin_yr": "Annual Operating Margin",
        "cost_kg": "Prod. Cost per KG",
        "energy_cost_yr": "Annual Energy Cost",
        "notes_label": "Meeting Notes / Strategic Observations",
        "notes_placeholder": "Enter agreements, discounts or customer observations...",
        "roi_ann": "Annualized ROI",
        "roe_capex": "ROE (on CAPEX)",
        "yield_5y": "5-Year Total Return (Yield)",
        "factor_dist": "Profit Driver Distribution",
        "line_a": "Standard Line",
        "line_b": "Premium Line"
    },
    "Italiano": {
        "title": "ROI Extrusion Strategic Advisor",
        "tech_comp": "📊 Comparazione Tecnica ed Operativa",
        "fin_comp": "💰 Performance Asset e Rendimento Finanziario",
        "res_title": "🏁 Risultati Analisi ROI",
        "download_pdf": "📩 Scarica Report Strategico COMPLETO (PDF)",
        "annual_prod": "Produzione Annua Netta",
        "margin_yr": "Margine Operativo Annuo",
        "cost_kg": "Costo al KG",
        "energy_cost_yr": "Costo Energia Annuo",
        "notes_label": "Note del Meeting / Osservazioni Strategiche",
        "notes_placeholder": "Inserisci accordi, sconti o osservazioni del cliente...",
        "roi_ann": "ROI Annualizzato",
        "roe_capex": "ROE (sul CAPEX)",
        "yield_5y": "Rendimento Totale a 5 Anni (Yield)",
        "factor_dist": "Contributo dei Fattori di Guadagno",
        "line_a": "Linea Standard",
        "line_b": "Linea Premium"
    },
    "Deutsch": {
        "title": "ROI Extrusion Strategic Advisor",
        "tech_comp": "📊 Technischer & Operativer Vergleich",
        "fin_comp": "💰 Asset-Performance & Finanzrendite",
        "res_title": "🏁 ROI-Analyseergebnisse",
        "download_pdf": "📩 Vollständigen Strategiebericht herunterladen (PDF)",
        "annual_prod": "Jährliche Nettoproduktion",
        "margin_yr": "Jährliche operativer Marge",
        "cost_kg": "Prod.-Kosten pro KG",
        "energy_cost_yr": "Jährliche Energiekosten",
        "notes_label": "Besprechungsnotizen / Strategische Beobachtungen",
        "notes_placeholder": "Vereinbarungen, Rabatte oder Kundenbeobachtungen eingeben...",
        "roi_ann": "Annualisierter ROI",
        "roe_capex": "ROE (auf CAPEX)",
        "yield_5y": "5-Jahres-Gesamtrendite (Yield)",
        "factor_dist": "Verteilung der Gewinnfaktoren",
        "line_a": "Standard-Linie",
        "line_b": "Premium-Linie"
    },
    "Español": {
        "title": "ROI Extrusion Strategic Advisor",
        "tech_comp": "📊 Comparativa Técnica y Operativa",
        "fin_comp": "💰 Rendimiento del Activo y Rendimiento Financiero",
        "res_title": "🏁 Resultados del Análisis ROI",
        "download_pdf": "📩 Descargar Informe Estratégico COMPLETO (PDF)",
        "annual_prod": "Producción Neta Anual",
        "margin_yr": "Margen Operativo Anual",
        "cost_kg": "Costo de Prod. por KG",
        "energy_cost_yr": "Costo de Energía Anual",
        "notes_label": "Notas de la reunión / Observaciones estratégicas",
        "notes_placeholder": "Ingrese acuerdos, descuentos u observaciones del cliente...",
        "roi_ann": "ROI Anualizado",
        "roe_capex": "ROE (sobre CAPEX)",
        "yield_5y": "Rendimiento Total a 5 años (Yield)",
        "factor_dist": "Distribución de los factores de beneficio",
        "line_a": "Línea Estándar",
        "line_b": "Línea Premium"
    }
}

st.set_page_config(page_title="ROI Extrusion", layout="wide")
lingua = st.sidebar.selectbox("Language / Lingua / Sprache / Idioma", ["English", "Italiano", "Deutsch", "Español"])
t = lang_dict[lingua]
st.title(t['title'])

# --- SIDEBAR: MERCATO ---
st.sidebar.header("🌍 Market Settings")
valuta_sel = st.sidebar.radio("Currency", ["EUR", "USD"])
cambio = 1.0; simbolo = "EUR"
if valuta_sel == "USD":
    cambio = st.sidebar.number_input("Exchange Rate (1€ = X $)", value=1.08)
    simbolo = "USD"

c_poly = st.sidebar.number_input(f"Polymer Cost ({simbolo}/kg)", value=1.40 * cambio) / cambio
p_sell = st.sidebar.number_input(f"Selling Price ({simbolo}/kg)", value=2.10 * cambio) / cambio
c_ene = st.sidebar.number_input(f"Energy Cost ({simbolo}/kWh)", value=0.22 * cambio) / cambio
h_an = st.sidebar.number_input("Hours/Year", value=8000)
tol_m = st.sidebar.slider("Market Tol. (±%)", 1.0, 10.0, 6.0)

# --- INPUT COMPARAZIONE ---
col_a, col_p = st.columns(2)
with col_a:
    st.subheader(f"⚪ {t['line_a']}")
    ca = st.number_input("CAPEX Standard", value=1500000)
    pa = st.number_input("Output (kg/h) Std", value=400)
    oa = st.number_input("OEE (%) Std", value=83.0)
    sa = st.number_input("2-Sigma (%) Std", value=3.5)
    scra = st.number_input("Scrap (%) Std", value=2.0)
    ma_std = st.number_input("Maint. % Std", value=2.5)
    csa = st.number_input("kWh/kg Std", value=0.40)

with col_p:
    st.subheader(f"💎 {t['line_b']}")
    cp = st.number_input("CAPEX Premium", value=2000000)
    pp = st.number_input("Output (kg/h) Prem", value=440)
    op = st.number_input("OEE (%) Prem", value=87.0)
    sp = st.number_input("2-Sigma (%) Prem", value=1.5)
    scrp = st.number_input("Scrap (%) Prem", value=1.5)
    mp_pre = st.number_input("Maint. % Prem", value=1.5)
    csp = st.number_input("kWh/kg Prem", value=0.35)

# --- CALCOLI AVANZATI ---
ton_a = (pa * h_an * (oa/100) * (1 - scra/100)) / 1000
ton_p = (pp * h_an * (op/100) * (1 - scrp/100)) / 1000

ene_cost_a = (pa * h_an * (oa/100) * csa * c_ene)
ene_cost_p = (pp * h_an * (op/100) * csp * c_ene)

opexa = (pa*h_an*(oa/100)*c_poly) + ene_cost_a + (ca*(ma_std/100))
opexp = (pp*h_an*(op/100)*c_poly*(1-(tol_m-sp)/100)) + ene_cost_p + (cp*(mp_pre/100))

marga, margp = (ton_a*1000*p_sell) - opexa, (ton_p*1000*p_sell) - opexp
dmarg = margp - marga
pbk = (cp - ca) / dmarg if dmarg > 0 else 0

roi_ann_a = (marga / ca) * 100
roi_ann_p = (margp / cp) * 100
roe_a = ((marga - (ca/10)) / ca) * 100
roe_p = ((margp - (cp/10)) / cp) * 100
yield_5y_a = ((marga * 5) / ca) * 100
yield_5y_p = ((margp * 5) / cp) * 100

# --- UI: TABELLE ---
st.subheader(t['tech_comp'])
df_tech = pd.DataFrame({
    "Metric": ["Output Real", "Efficiency (OEE)", "Material Scrap", "Specific Cons.", "Maintenance"],
    "Standard": [f"{pa} kg/h", f"{oa}%", f"{scra}%", f"{csa} kWh/kg", f"{ma_std}%"],
    "Premium": [f"{pp} kg/h", f"{op}%", f"{scrp}%", f"{csp} kWh/kg", f"{mp_pre}%"],
    "Delta": [f"+{pp-pa}", f"+{op-oa}%", f"-{scra-scrp}%", f"-{csa-csp}", f"-{ma_std-mp_pre}%"]
})
st.table(df_tech)

st.subheader(t['fin_comp'])
df_fin = pd.DataFrame({
    "Financial Indicator": [t['margin_yr'], t['roi_ann'], t['roe_capex'], t['yield_5y']],
    "Standard": [f"{simbolo} {marga*cambio:,.0f}", f"{roi_ann_a:.1f}%", f"{roe_a:.1f}%", f"{yield_5y_a:.1f}%"],
    "Premium": [f"{simbolo} {margp*cambio:,.0f}", f"{roi_ann_p:.1f}%", f"{roe_p:.1f}%", f"{yield_5y_p:.1f}%"],
    "Advantage": ["-", f"+{roi_ann_p-roi_ann_a:.1f}%", f"+{roe_p-roe_a:.1f}%", f"+{yield_5y_p-yield_5y_a:.1f}%"]
})
st.table(df_fin)

# --- GRAFICI ---
st.header(t['res_title'])
c1, c2 = st.columns(2)
with c1:
    gain_prod = (ton_p - ton_a) * 1000 * (p_sell - c_poly)
    gain_precision = (pp * h_an * (op/100)) * c_poly * ((tol_m - sp)/100 - (tol_m - sa)/100)
    gain_maint = (ca * ma_std/100) - (cp * mp_pre/100)
    gain_energy = (pa * h_an * (oa/100)) * (csa - csp) * c_ene
    fig_pie = go.Figure(data=[go.Pie(labels=['Prod.', 'Precision', 'Energy', 'Maint.'], 
                                    values=[gain_prod, gain_precision, gain_energy, gain_maint], hole=.4)])
    fig_pie.update_layout(title=t['factor_dist'])
    st.plotly_chart(fig_pie, use_container_width=True)
with c2:
    yrs = list(range(11))
    fa = [(-ca + (marga * i)) * cambio for i in yrs]
    fp = [(-cp + (margp * i)) * cambio for i in yrs]
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=yrs, y=fa, name="Standard", line=dict(color='gray', dash='dot')))
    fig_line.add_trace(go.Scatter(x=yrs, y=fp, name="Premium", line=dict(color='#00CC96', width=4)))
    fig_line.update_layout(title="Cash Flow")
    st.plotly_chart(fig_line, use_container_width=True)

st.divider()
meeting_notes = st.text_area(t['notes_label'], placeholder=t['notes_placeholder'], height=150)

# --- PDF GENERATOR ---
def create_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(190, 10, "STRATEGIC ROI REPORT", ln=True, align='C')
    
    # Tabelle
    pdf.ln(5); pdf.set_font("Arial", "B", 12); pdf.set_fill_color(230, 230, 230)
    pdf.cell(190, 10, " 1. TECHNICAL & FINANCIAL SUMMARY", ln=True, fill=True)
    pdf.set_font("Arial", "", 9)
    for i, row in df_tech.iterrows():
        pdf.cell(50, 7, row['Metric'], 1); pdf.cell(70, 7, row['Standard'], 1); pdf.cell(70, 7, row['Premium'], 1, 1)
    
    pdf.ln(5); pdf.set_font("Arial", "B", 10)
    pdf.cell(50, 7, "Yield Analysis", 1, fill=True); pdf.cell(70, 7, f"Standard: {yield_5y_a:.1f}%", 1); pdf.cell(70, 7, f"Premium: {yield_5y_p:.1f}%", 1, 1)

    # Spazio per i grafici (Spostati in basso per evitare sovrapposizioni)
    pdf.ln(10) 
    curr_y = pdf.get_y()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        p1 = os.path.join(tmpdir, "p1.png"); p2 = os.path.join(tmpdir, "p2.png")
        # Forzo colori e sfondo bianco per l'esportazione
        fig_pie.write_image(p1, engine="kaleido", scale=2)
        fig_line.write_image(p2, engine="kaleido", scale=2)
        
        pdf.image(p1, x=10, y=curr_y, w=90)
        pdf.image(p2, x=105, y=curr_y, w=90)

    if meeting_notes:
        pdf.set_y(curr_y + 80) # Posiziona le note sotto i grafici
        pdf.set_font("Arial", "B", 12)
        pdf.cell(190, 10, " 2. STRATEGIC NOTES", ln=True, fill=True)
        pdf.set_font("Arial", "", 10); pdf.multi_cell(190, 7, meeting_notes, 1)
        
    return pdf.output(dest='S').encode('latin-1', 'replace')

if st.button(t['download_pdf']):
    st.download_button("Download PDF", data=create_pdf(), file_name="ROI_Report.pdf", mime="application/pdf")
