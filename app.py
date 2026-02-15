import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from fpdf import FPDF

# 1. TRADUZIONI
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
        "res_title": "ROI Analysis Results",
        "tech_comp": "Comparative Performance Table",
        "extra_margin": "Extra Annual Margin",
        "payback": "Payback (Years)",
        "cost_kg": "Prod. Cost per KG",
        "profit_5y": "Extra Profit (5y)",
        "extra_tons": "Extra Yearly Production",
        "annual_prod": "Annual Net Production",
        "download_pdf": "📩 Download PDF Report",
        "diff_col": "Difference"
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
        "res_title": "Risultati Analisi ROI",
        "tech_comp": "Tabella Comparativa Prestazioni",
        "extra_margin": "Extra Margine Annuo",
        "payback": "Pareggio (Anni)",
        "cost_kg": "Costo al KG",
        "profit_5y": "Extra Profitto (5 anni)",
        "extra_tons": "Tonnellate Extra / Anno",
        "annual_prod": "Produzione Annua Netta",
        "download_pdf": "📩 Scarica Report PDF",
        "diff_col": "Differenza"
    }
}

# --- FUNZIONE PDF CORRETTA ---
def create_pdf(data_dict, lang_t, simbolo_text, val_code, line_a, line_p):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(190, 10, txt=lang_t['title'], ln=True, align='C')
    pdf.ln(5)
    
    # Sezione Economica
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, txt=lang_t['res_title'].upper(), ln=True, fill=False)
    pdf.set_font("Arial", "", 10)
    
    metrics = [
        (lang_t['extra_margin'], f"{simbolo_text} {data_dict['dmarg']:,.0f}"),
        (lang_t['extra_tons'], f"{data_dict['diff_tons']:,.0f} T/y"),
        (lang_t['payback'], f"{data_dict['pbk']:.1f} Yrs"),
        (lang_t['profit_5y'], f"{simbolo_text} {data_dict['p5y']:,.0f}")
    ]
    
    for m in metrics:
        pdf.cell(95, 8, m[0], 1)
        pdf.cell(95, 8, m[1], 1, 1, 'C')
    
    pdf.ln(10)
    
    # Tabella Tecnica
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, txt=lang_t['tech_comp'].upper(), ln=True)
    pdf.set_font("Arial", "B", 9)
    pdf.cell(60, 10, "Parameter", 1, 0, 'C')
    pdf.cell(65, 10, lang_t['line_a'], 1, 0, 'C')
    pdf.cell(65, 10, lang_t['line_b'], 1, 1, 'C')
    
    pdf.set_font("Arial", "", 9)
    tech_rows = [
        (lang_t['annual_prod'], f"{line_a['tons']:,.0f} T", f"{line_p['tons']:,.0f} T"),
        (lang_t['scrap'], f"{line_a['scr']}%", f"{line_p['scr']}%"),
        (lang_t['oee'], f"{line_a['oee']}%", f"{line_p['oee']}%"),
        (lang_t['cost_kg'], f"{simbolo_text} {line_a['ckg']:.3f}", f"{simbolo_text} {line_p['ckg']:.3f}")
    ]
    
    for r in tech_rows:
        pdf.cell(60, 8, r[0], 1)
        pdf.cell(65, 8, r[1], 1, 0, 'C')
        pdf.cell(65, 8, r[2], 1, 1, 'C')

    return pdf.output(dest='S').encode('latin-1', 'replace')

# --- UI STREAMLIT ---
st.set_page_config(page_title="ROI Extrusion", layout="wide")
lingua = st.sidebar.selectbox("Language", ["English", "Italiano"])
t = lang_dict[lingua]

# Currency logic
valuta_sel = st.sidebar.radio("Currency", ["EUR", "USD"])
cambio = 1.0; simbolo_text = "EUR"
if valuta_sel == "USD":
    cambio = st.sidebar.number_input(t['exchange_rate'], value=1.08)
    simbolo_text = "USD"

# Input
col_a, col_p = st.columns(2)
with col_a:
    st.subheader(t['line_a'])
    ca = st.number_input(f"CAPEX A", value=1500000)
    pa = 400; oa = 75.0; scra = 4.0
with col_p:
    st.subheader(t['line_b'])
    cp = st.number_input(f"CAPEX Premium", value=2000000)
    pp = 440; op = 85.0; scrp = 1.5

# Calcoli semplificati per test
ton_a = (pa * 8000 * (oa/100) * (1 - scra/100)) / 1000
ton_p = (pp * 8000 * (op/100) * (1 - scrp/100)) / 1000
dmarg = (ton_p - ton_a) * 1000 * 0.5 # Esempio margine
p5y = (dmarg * 5) - (cp - ca)
pbk = (cp - ca) / dmarg if dmarg > 0 else 0

# Display
st.divider()
c1, c2, c3 = st.columns(3)
c1.metric(t['extra_margin'], f"{simbolo_text} {dmarg*cambio:,.0f}")
c2.metric(t['extra_tons'], f"{ton_p - ton_a:,.0f} T")
c3.metric(t['payback'], f"{pbk:.1f} Yrs")

# PDF Data Preparation
l_a_data = {'tons': ton_a, 'scr': scra, 'oee': oa, 'ckg': 1.20} # Valori esempio
l_p_data = {'tons': ton_p, 'scr': scrp, 'oee': op, 'ckg': 1.15}

if st.button(t['download_pdf']):
    pdf_bytes = create_pdf({'dmarg': dmarg*cambio, 'diff_tons': ton_p-ton_a, 'pbk': pbk, 'p5y': p5y*cambio}, t, simbolo_text, valuta_sel, l_a_data, l_p_data)
    st.download_button("Click here to save PDF", data=pdf_bytes, file_name="ROI_Report.pdf", mime="application/pdf")
