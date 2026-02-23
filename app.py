import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from fpdf import FPDF
import tempfile
import os
import re

# Funzione per pulire il testo per il PDF
def clean_text(text):
    if text is None: return ""
    return re.sub(r'[^\x00-\xff]+', '', str(text))

# --- 1. DIZIONARIO TRADUZIONI COMPLETO ---
lang_dict = {
    "English": {
        "title": "ROI Extrusion Strategic Advisor",
        "tech_comp": "📊 Technical & Operational Comparison",
        "fin_comp": "💰 Asset Performance & Financial Yield",
        "res_title": "🏁 ROI Analysis Results",
        "download_pdf": "📩 Download RICH Strategic Report (PDF)",
        "line_a": "Standard Line",
        "line_b": "Premium Line",
        "line_c": "Fusion Line",
        "notes_label": "Executive Observations",
        "notes_placeholder": "Enter strategic notes...",
        "payback_label": "Payback Period (Years)",
        "crossover_title": "Cumulative Extra Profit (vs Std)",
        "t_prod": "Annual Production",
        "t_oee": "Efficiency (OEE)",
        "t_scrap": "Material Scrap",
        "t_cons": "Spec. Consumption",
        "chart_years": "Years",
        "chart_profit": "Net Surplus",
        "cost_kg": "Unit Cost (€/kg)",
        "margin_yr": "Annual Op. Margin",
        "roi_ann": "Annualized ROI",
        "extra_5y": "5-Year Extra Profit",
        "market_settings": "Market Scenario & Unit Costs",
        "exec_summary": "Executive Financial Summary"
    },
    "Italiano": {
        "title": "ROI Extrusion Strategic Advisor",
        "tech_comp": "📊 Comparazione Tecnica ed Operativa",
        "fin_comp": "💰 Performance Asset e Rendimento Finanziario",
        "res_title": "🏁 Risultati Analisi ROI",
        "download_pdf": "📩 Scarica Report Strategico AVANZATO (PDF)",
        "line_a": "Linea Standard",
        "line_b": "Linea Premium",
        "line_c": "Linea Fusion",
        "notes_label": "Osservazioni Executive",
        "notes_placeholder": "Inserisci note strategiche...",
        "payback_label": "Periodo di Payback (Anni)",
        "crossover_title": "Extra Profitto Cumulativo (vs Std)",
        "t_prod": "Produzione Annua",
        "t_oee": "Efficienza (OEE)",
        "t_scrap": "Scarto Materiale",
        "t_cons": "Consumo Specifico",
        "chart_years": "Anni",
        "chart_profit": "Surplus Netto",
        "cost_kg": "Costo Unitario (€/kg)",
        "margin_yr": "Margine Op. Annuo",
        "roi_ann": "ROI Annualizzato",
        "extra_5y": "Extra Profitto 5 Anni",
        "market_settings": "Scenario di Mercato e Costi Unitari",
        "exec_summary": "Sintesi Finanziaria Executive"
    },
    "Deutsch": {
        "title": "ROI Extrusion Strategic Advisor",
        "tech_comp": "📊 Technischer Vergleich",
        "fin_comp": "💰 Finanzrendite",
        "res_title": "🏁 ROI-Ergebnisse",
        "download_pdf": "📩 Strategischen Bericht herunterladen (PDF)",
        "line_a": "Standard",
        "line_b": "Premium",
        "line_c": "Fusion",
        "notes_label": "Strategische Notizen",
        "notes_placeholder": "Notizen eingeben...",
        "payback_label": "Amortisation (Jahre)",
        "crossover_title": "Zusatzgewinn (vs Std)",
        "t_prod": "Produktion/Jahr",
        "t_oee": "Effizienz (OEE)",
        "t_scrap": "Ausschuss",
        "t_cons": "Energieverbrauch",
        "chart_years": "Jahre",
        "chart_profit": "Nettoüberschuss",
        "cost_kg": "Stückkosten (€/kg)",
        "margin_yr": "Operative Marge",
        "roi_ann": "ROI p.a.",
        "extra_5y": "5-Jahres-Zusatzprofit",
        "market_settings": "Marktszenario",
        "exec_summary": "Finanzielle Zusammenfassung"
    },
    "Español": {
        "title": "ROI Extrusion Strategic Advisor",
        "tech_comp": "📊 Comparativa Técnica",
        "fin_comp": "💰 Rendimiento Financiero",
        "res_title": "🏁 Resultados ROI",
        "download_pdf": "📩 Descargar Informe Detallado (PDF)",
        "line_a": "Estándar",
        "line_b": "Premium",
        "line_c": "Fusion",
        "notes_label": "Notas Estratégicas",
        "notes_placeholder": "Escribir observaciones...",
        "payback_label": "Payback (Años)",
        "crossover_title": "Beneficio Extra (vs Std)",
        "t_prod": "Producción Anual",
        "t_oee": "Eficiencia (OEE)",
        "t_scrap": "Desperdicio",
        "t_cons": "Consumo Específico",
        "chart_years": "Años",
        "chart_profit": "Excedente Neto",
        "cost_kg": "Costo Unitario (€/kg)",
        "margin_yr": "Margen Operativo",
        "roi_ann": "ROI Anualizado",
        "extra_5y": "Beneficio Extra 5 años",
        "market_settings": "Contexto de Mercado",
        "exec_summary": "Resumen Financiero Ejecutivo"
    }
}

st.set_page_config(page_title="ROI Strategic Advisor", layout="wide")
lingua = st.sidebar.selectbox("Language", list(lang_dict.keys()), index=0)
t = lang_dict[lingua]
st.title(t['title'])

# --- SIDEBAR & CALCULATIONS (Semplificati per brevità ma completi) ---
st.sidebar.header("🌍 Market Context")
valuta = st.sidebar.radio("Currency", ["EUR", "USD"])
simbolo = "€" if valuta == "EUR" else "$"
cambio = st.sidebar.number_input("Exchange Rate", value=1.0) if valuta == "USD" else 1.0

# Input CAPEX e parametri
with st.sidebar:
    c_poly = st.number_input("Polymer Cost/kg", value=1.5)
    p_sell = st.number_input("Selling Price/kg", value=2.2)
    c_ene = st.number_input("Energy Cost/kWh", value=0.20)
    h_an = st.number_input("Working Hours/Year", value=7000)
    show_fusion = checkbox_f = st.checkbox("Fusion Line")

# Funzione metrica core
def calc_all(p, o, s, scr, cs, m, cap, cp):
    ton = (p * h_an * (o/100) * (1 - scr/100)) / 1000
    opex = (p * h_an * (o/100) * cp * (1-(6-s)/100)) + (p * h_an * (o/100) * cs * c_ene) + (cap * m/100)
    marg = (ton * 1000 * p_sell) - opex
    ckg = opex / (ton * 1000)
    pb = cap / marg if marg > 0 else 0
    return ton, marg, ckg, pb, opex

# Dati Macchine (Standard, Premium, Fusion)
ton_a, marg_a, ckg_a, pb_a, opex_a = calc_all(400, 83, 3.5, 2.0, 0.40, 2.5, 1500000, c_poly)
ton_b, marg_b, ckg_b, pb_b, opex_b = calc_all(440, 88, 1.5, 1.2, 0.32, 1.5, 2100000, c_poly)
if show_fusion:
    ton_c, marg_c, ckg_c, pb_c, opex_c = calc_all(440, 90, 1.0, 0.8, 0.25, 1.2, 2400000, c_poly * 0.9)

# --- UI: TABELLE ---
st.subheader(t['tech_comp'])
df_t = pd.DataFrame({
    "Metric": [t['t_prod'], t['t_oee'], t['t_scrap'], t['t_cons']],
    "Standard": [f"{ton_a:,.0f} T", "83%", "2.0%", "0.40"],
    "Premium": [f"{ton_b:,.0f} T", "88%", "1.2%", "0.32"]
})
if show_fusion: df_t["Fusion"] = [f"{ton_c:,.0f} T", "90%", "0.8%", "0.25"]
st.table(df_t)

st.subheader(t['fin_comp'])
df_f = pd.DataFrame({
    "Indicator": [t['cost_kg'], t['margin_yr'], t['roi_ann'], t['payback_label'], t['extra_5y']],
    "Standard": [f"{ckg_a:.3f}", f"{marg_a:,.0f}", f"{(marg_a/1500000)*100:.1f}%", f"{pb_a:.1f}", "-"],
    "Premium": [f"{ckg_b:.3f}", f"{marg_b:,.0f}", f"{(marg_b/2100000)*100:.1f}%", f"{pb_b:.1f}", f"{(marg_b-marg_a)*5:,.0f}"]
})
if show_fusion: df_f["Fusion"] = [f"{ckg_c:.3f}", f"{marg_c:,.0f}", f"{(marg_c/2400000)*100:.1f}%", f"{pb_c:.1f}", f"{(marg_c-marg_a)*5:,.0f}"]
st.table(df_f)

# --- GRAFICI ---
c1, c2 = st.columns(2)
with c1:
    fig_pb = go.Figure(go.Bar(x=[pb_a, pb_b, pb_c] if show_fusion else [pb_a, pb_b], y=[t['line_a'], t['line_b'], t['line_c']] if show_fusion else [t['line_a'], t['line_b']], orientation='h'))
    fig_pb.update_layout(title=t['payback_label'])
    st.plotly_chart(fig_pb)

with c2:
    yrs = list(range(6))
    fig_cross = go.Figure()
    fig_cross.add_trace(go.Scatter(x=yrs, y=[(-(2100000-1500000)+(marg_b-marg_a)*y) for y in yrs], name="Premium vs Std"))
    if show_fusion:
        fig_cross.add_trace(go.Scatter(x=yrs, y=[(-(2400000-1500000)+(marg_c-marg_a)*y) for y in yrs], name="Fusion vs Std"))
    fig_cross.update_layout(title=t['crossover_title'])
    st.plotly_chart(fig_cross)

notes = st.text_area(t['notes_label'], height=100)

# --- GENERAZIONE PDF RICCO ---
if st.button(t['download_pdf']):
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(40, 70, 120)
    pdf.cell(190, 15, clean_text(t['title']), ln=True, align='C')
    
    # Executive Summary Section
    pdf.ln(10)
    pdf.set_fill_color(230, 235, 245)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(190, 10, clean_text(t['exec_summary']), ln=True, fill=True)
    pdf.set_font("Arial", '', 11)
    pdf.set_text_color(0)
    pdf.ln(5)
    summary_txt = f"Analysis based on {h_an} annual hours. Polymer market cost: {simbolo}{c_poly}/kg. " \
                  f"The Premium Line reduces unit cost by {((ckg_a-ckg_b)/ckg_a)*100:.1f}% compared to Standard."
    pdf.multi_cell(190, 7, clean_text(summary_txt))
    
    # Financial Comparison Table
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(190, 10, "Table 1: Financial KPI Comparison", ln=True)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(45, 10, "Indicator", 1, 0, 'C', True)
    pdf.cell(45, 10, "Standard", 1, 0, 'C', True)
    pdf.cell(45, 10, "Premium", 1, 0, 'C', True)
    if show_fusion: pdf.cell(45, 10, "Fusion", 1, 1, 'C', True)
    else: pdf.ln()
    
    pdf.set_font("Arial", '', 10)
    for _, row in df_f.iterrows():
        pdf.cell(45, 10, clean_text(row['Indicator']), 1)
        pdf.cell(45, 10, clean_text(row['Standard']), 1)
        pdf.cell(45, 10, clean_text(row['Premium']), 1)
        if show_fusion: pdf.cell(45, 10, clean_text(row['Fusion']), 1, 1)
        else: pdf.ln()

    # Inserimento Grafici (Kaleido)
    with tempfile.TemporaryDirectory() as tmpdir:
        # Salvataggio grafico 1
        img1_path = os.path.join(tmpdir, "chart1.png")
        fig_pb.write_image(img1_path)
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(190, 10, "Chart 1: Investment Payback Benchmark", ln=True)
        pdf.image(img1_path, x=15, w=170)
        
        # Salvataggio grafico 2
        pdf.add_page()
        img2_path = os.path.join(tmpdir, "chart2.png")
        fig_cross.write_image(img2_path)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(190, 10, "Chart 2: Cumulative Extra Profit vs Time", ln=True)
        pdf.image(img2_path, x=15, w=170)

    # Strategic Notes
    if notes:
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(190, 10, clean_text(t['notes_label']), ln=True, fill=True)
        pdf.set_font("Arial", 'I', 11)
        pdf.multi_cell(190, 8, clean_text(notes))

    # Output
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        with open(tmp.name, "rb") as f:
            st.download_button(t['download_pdf'], f, file_name="Extrusion_ROI_Strategic_Report.pdf")
