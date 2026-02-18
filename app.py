import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from fpdf import FPDF
import tempfile
import os

# 1. DIZIONARIO TRADUZIONI COMPLETO
lang_dict = {
    "English": {
        "title": "ROI Extrusion",
        "line_a": "Standard Line",
        "line_b": "Premium Line",
        "res_title": "🏁 ROI Analysis Results",
        "tech_comp": "📊 Comparative Performance & Differences",
        "download_pdf": "📩 Download FULL Strategic Report (PDF)",
        "extra_tons": "Extra Tons/Year",
        "payback": "Payback (Years)",
        "profit_5y": "5y Extra Profit",
        "cost_kg": "Prod. Cost per KG",
        "annual_prod": "Annual Net Production",
        "margin_yr": "Annual Margin",
        "exchange_rate": "Exchange Rate (1€ = X $)",
        "output_h": "Hourly Output",
        "notes_label": "Meeting Notes / Comments",
        "notes_placeholder": "Enter meeting agreements or customer observations here...",
        "energy_cost_yr": "Annual Energy Cost",
        "energy_save": "Energy Saving (Premium)",
        "factor_dist": "Contribution to Extra Margin"
    },
    "Italiano": {
        "title": "ROI Extrusion",
        "line_a": "Linea Standard",
        "line_b": "Linea Premium",
        "res_title": "🏁 Risultati Analisi ROI",
        "tech_comp": "📊 Comparazione Performance e Differenze",
        "download_pdf": "📩 Scarica Report Strategico COMPLETO (PDF)",
        "extra_tons": "Tonnellate Extra/Anno",
        "payback": "Pareggio (Anni)",
        "profit_5y": "Extra Profitto (5 anni)",
        "cost_kg": "Costo al KG",
        "annual_prod": "Produzione Annua Netta",
        "margin_yr": "Margine Annuo",
        "exchange_rate": "Tasso di Cambio (1€ = X $)",
        "output_h": "Portata Oraria",
        "notes_label": "Note del Meeting / Commenti",
        "notes_placeholder": "Inserisci qui gli accordi presi o le osservazioni del cliente...",
        "energy_cost_yr": "Costo Energia Annuo",
        "energy_save": "Risparmio Energetico (Premium)",
        "factor_dist": "Contributo ai Fattori di Guadagno"
    },
    "Deutsch": {
        "title": "ROI Extrusion",
        "line_a": "Standard-Linie",
        "line_b": "Premium-Linie",
        "res_title": "🏁 ROI-Analyseergebnisse",
        "tech_comp": "📊 Leistungsvergleich & Unterschiede",
        "download_pdf": "📩 Vollständigen Bericht herunterladen (PDF)",
        "extra_tons": "Zusätzliche Tonnen/Jahr",
        "payback": "Amortisation (Jahre)",
        "profit_5y": "Extra-Profit (5 J.)",
        "cost_kg": "Prod.-Kosten pro KG",
        "annual_prod": "Jährliche Nettoproduktion",
        "margin_yr": "Jährliche Marge",
        "exchange_rate": "Wechselkurs (1€ = X $)",
        "output_h": "Stundenleistung",
        "notes_label": "Besprechungsnotizen",
        "notes_placeholder": "Geben Sie hier Vereinbarungen oder Kundenbeobachtungen ein...",
        "energy_cost_yr": "Jährliche Energiekosten",
        "energy_save": "Energieersparnis (Premium)",
        "factor_dist": "Beitrag zum Extra-Margen"
    },
    "Español": {
        "title": "ROI Extrusion",
        "line_a": "Línea Estándar",
        "line_b": "Línea Premium",
        "res_title": "🏁 Resultados del Análisis ROI",
        "tech_comp": "📊 Comparativa de Rendimiento y Diferencias",
        "download_pdf": "📩 Descargar Informe Estratégico COMPLETO (PDF)",
        "extra_tons": "Toneladas Extra/Año",
        "payback": "Retorno (Años)",
        "profit_5y": "Extra Beneficio (5a)",
        "cost_kg": "Costo de Prod. por KG",
        "annual_prod": "Producción Neta Anual",
        "margin_yr": "Margen Anual",
        "exchange_rate": "Tipo de Cambio (1€ = X $)",
        "output_h": "Capacidad Horaria",
        "notes_label": "Notas de la reunión",
        "notes_placeholder": "Ingrese aquí los acuerdos o las observaciones del cliente...",
        "energy_cost_yr": "Costo de Energía Anual",
        "energy_save": "Ahorro de Energía (Premium)",
        "factor_dist": "Contribución al Margen Extra"
    }
}

st.set_page_config(page_title="ROI Extrusion", layout="wide")

lingua = st.sidebar.selectbox("Language / Lingua / Sprache / Idioma", ["English", "Italiano", "Deutsch", "Español"])
t = lang_dict[lingua]

st.title(t['title'])

# --- SIDEBAR: MERCATO ---
st.sidebar.header("🌍 Market Settings")
valuta_sel = st.sidebar.radio("Currency / Valuta", ["EUR", "USD"])
cambio = 1.0; simbolo = "EUR"
if valuta_sel == "USD":
    cambio = st.sidebar.number_input(t['exchange_rate'], value=1.08)
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
    pa = st.number_input(f"{t['output_h']} Std (kg/h)", value=400)
    oa = st.number_input("OEE (%) Standard", value=83.0)
    sa = st.number_input("2-Sigma (%) Standard", value=3.5)
    scra = st.number_input("Scrap (%) Standard", value=2.0)
    ma_std = st.number_input("Maint. Cost (% CAPEX) Std", value=2.5)
    csa = st.number_input("Specific Consumption (kWh/kg) Std", value=0.40)

with col_p:
    st.subheader(f"💎 {t['line_b']}")
    cp = st.number_input("CAPEX Premium", value=2000000)
    pp = st.number_input(f"{t['output_h']} Prem (kg/h)", value=440)
    op = st.number_input("OEE (%) Premium", value=87.0)
    sp = st.number_input("2-Sigma (%) Premium", value=1.5)
    scrp = st.number_input("Scrap (%) Premium", value=1.5)
    mp_pre = st.number_input("Maint. Cost (% CAPEX) Prem", value=1.5)
    csp = st.number_input("Specific Consumption (kWh/kg) Prem", value=0.35)

# --- CALCOLI AVANZATI ---
ton_a = (pa * h_an * (oa/100) * (1 - scra/100)) / 1000
ton_p = (pp * h_an * (op/100) * (1 - scrp/100)) / 1000
diff_tons = ton_p - ton_a

ene_cost_a = (pa * h_an * (oa/100) * csa * c_ene)
ene_cost_p = (pp * h_an * (op/100) * csp * c_ene)

opexa = (pa*h_an*(oa/100)*c_poly) + ene_cost_a + (ca*(ma_std/100))
opexp = (pp*h_an*(op/100)*c_poly*(1-(tol_m-sp)/100)) + ene_cost_p + (cp*(mp_pre/100))

ckga = (opexa + (ca/10)) / (ton_a*1000) if ton_a > 0 else 0
ckgp = (opexp + (cp/10)) / (ton_p*1000) if ton_p > 0 else 0
marga, margp = (ton_a*1000*p_sell) - opexa, (ton_p*1000*p_sell) - opexp
dmarg = margp - marga
pbk = (cp - ca) / dmarg if dmarg > 0 else 0
p5y = (dmarg * 5) - (cp - ca)

# Analisi Fattori
gain_prod = (ton_p - ton_a) * 1000 * (p_sell - c_poly)
gain_precision = (pp * h_an * (op/100)) * c_poly * ((tol_m - sp)/100 - (tol_m - sa)/100)
gain_maint = (ca * ma_std/100) - (cp * mp_pre/100)
gain_energy = (pa * h_an * (oa/100)) * (csa - csp) * c_ene # Risparmio energetico su base oraria equivalente

# --- TABELLA UI ---
st.subheader(t['tech_comp'])
df_vis = pd.DataFrame({
    "Metric": [t['output_h'], t['annual_prod'], "OEE %", "Scrap %", "2-Sigma %", t['energy_cost_yr'], t['cost_kg'], t['margin_yr']],
    t['line_a']: [f"{pa} kg/h", f"{ton_a:,.0f} T", f"{oa}%", f"{scra}%", f"{sa}%", f"{simbolo} {ene_cost_a*cambio:,.0f}", f"{simbolo} {ckga*cambio:.3f}", f"{simbolo} {marga*cambio:,.0f}"],
    t['line_b']: [f"{pp} kg/h", f"{ton_p:,.0f} T", f"{op}%", f"{scrp}%", f"{sp}%", f"{simbolo} {ene_cost_p*cambio:,.0f}", f"{simbolo} {ckgp*cambio:.3f}", f"{simbolo} {margp*cambio:,.0f}"],
    "Analysis": [f"🚀 +{pp-pa} kg/h", f"📈 +{diff_tons:,.0f} T", f"✅ +{op-oa}%", f"📉 -{scra-scrp}%", f"🎯 {sp-sa}%", f"⚡ {simbolo} {(ene_cost_a - ene_cost_p)*cambio:,.0f}", f"💸 -{simbolo} {(ckga-ckgp)*cambio:.3f}", f"🔥 +{simbolo} {dmarg*cambio:,.0f}"]
})
st.table(df_vis)

# --- SEZIONE ROI ---
st.header(t['res_title'])
with st.container():
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"### <span style='color:#00CC96'>{simbolo} {dmarg*cambio:,.0f}</span>", unsafe_allow_html=True)
    c1.caption(f"**{t['margin_yr']} Extra**")
    c2.markdown(f"### <span style='color:#00CC96'>+{diff_tons:,.0f} T</span>", unsafe_allow_html=True)
    c2.caption(f"**{t['extra_tons']}**")
    c3.markdown(f"### <span style='color:#FF4B4B'>{pbk:.1f} Yrs</span>", unsafe_allow_html=True)
    c3.caption(f"**{t['payback']}**")
    c4.markdown(f"### <span style='color:#00CC96'>{simbolo} {p5y*cambio:,.0f}</span>", unsafe_allow_html=True)
    c4.caption(f"**{t['profit_5y']}**")

# --- GRAFICI ---
col_g1, col_g2 = st.columns(2)
with col_g1:
    labels = ['Extra Productivity', 'Material Precision', 'Energy Saving', 'Maintenance Delta']
    values = [max(0, gain_prod), max(0, gain_precision), max(0, gain_energy), max(0, gain_maint)]
    fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4, marker=dict(colors=['#00CC96', '#19D3F3', '#AB63FA', '#FFA15A']))])
    fig_pie.update_layout(title_text=t['factor_dist'])
    st.plotly_chart(fig_pie, use_container_width=True)

with col_g2:
    yrs = list(range(11))
    fa = [(-ca + (marga * i)) * cambio for i in yrs]
    fp = [(-cp + (margp * i)) * cambio for i in yrs]
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=yrs, y=fa, name=t['line_a'], line=dict(color='gray', dash='dot')))
    fig_line.add_trace(go.Scatter(x=yrs, y=fp, name=t['line_b'], line=dict(color='#00CC96', width=4)))
    fig_line.update_layout(title="Cumulative Cash Flow")
    st.plotly_chart(fig_line, use_container_width=True)

# --- NOTE ---
st.divider()
st.subheader(t['notes_label'])
meeting_notes = st.text_area("", placeholder=t['notes_placeholder'], height=150)

# --- FUNZIONE PDF CON GRAFICI ---
def create_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(190, 10, "ROI EXTRUSION - STRATEGIC REPORT", ln=True, align='C')
    
    # Dati Tabella
    pdf.ln(5); pdf.set_font("Arial", "B", 12); pdf.set_fill_color(240, 240, 240)
    pdf.cell(190, 10, " 1. TECHNICAL & FINANCIAL SUMMARY", ln=True, fill=True)
    pdf.set_font("Arial", "", 9)
    pdf.cell(60, 8, "Metric", 1); pdf.cell(65, 8, "STANDARD LINE", 1); pdf.cell(65, 8, "PREMIUM LINE", 1, 1)
    pdf.cell(60, 8, "Annual Margin", 1); pdf.cell(65, 8, f"{simbolo} {marga*cambio:,.0f}", 1); pdf.cell(65, 8, f"{simbolo} {margp*cambio:,.0f}", 1, 1)
    pdf.cell(60, 8, "Payback Period", 1); pdf.cell(65, 8, "-", 1); pdf.cell(65, 8, f"{pbk:.1f} Years", 1, 1)
    
    # Calcolo Rendimento Finanziario a 5 Anni
    yield_std = ((marga * 5) / ca) * 100
    yield_pre = ((margp * 5) / cp) * 100
    pdf.ln(5); pdf.set_font("Arial", "B", 10)
    pdf.cell(190, 8, f"Financial Yield (5-Year Total ROI): Standard {yield_std:.1f}% vs Premium {yield_pre:.1f}%", ln=True)

    # Esportazione e inserimento grafici
    with tempfile.TemporaryDirectory() as tmpdir:
        path_pie = os.path.join(tmpdir, "pie.png")
        path_line = os.path.join(tmpdir, "line.png")
        fig_pie.write_image(path_pie, engine="kaleido")
        fig_line.write_image(path_line, engine="kaleido")
        
        pdf.ln(5)
        pdf.image(path_pie, x=10, y=None, w=90)
        pdf.image(path_line, x=105, y=pdf.get_y() - 75, w=90) # Allineamento orizzontale

    if meeting_notes:
        pdf.set_y(220)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(190, 10, " 2. MEETING NOTES", ln=True, fill=True)
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(190, 8, meeting_notes, 1)
        
    return pdf.output(dest='S').encode('latin-1', 'replace')

st.divider()
if st.button(t['download_pdf']):
    # Nota: richiede 'kaleido' installato per salvare i grafici plotly come immagini
    try:
        st.download_button("Save Final Report PDF", data=create_pdf(), file_name="ROI_Extrusion_Report.pdf", mime="application/pdf")
    except Exception as e:
        st.error(f"Please install kaleido: `pip install kaleido`. Error: {e}")
