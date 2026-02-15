import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from fpdf import FPDF

# 1. TRADUZIONI E CONFIGURAZIONE
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
        "cost_kg": "Prod. Cost per KG"
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
        "cost_kg": "Costo al KG"
    }
}

st.set_page_config(page_title="ROI Extrusion", layout="wide")
lingua = st.sidebar.selectbox("Lingua/Language", ["Italiano", "English"])
t = lang_dict[lingua]

st.title(t['title'])

# --- SIDEBAR CURRENCY & MARKET ---
valuta_sel = st.sidebar.radio("Valuta/Currency", ["EUR", "USD"])
cambio = 1.0; simbolo = "EUR"
if valuta_sel == "USD":
    cambio = st.sidebar.number_input("Tasso Cambio (1€ = X $)", value=1.08)
    simbolo = "USD"

st.sidebar.divider()
c_poly = st.sidebar.number_input(f"Costo Polimero ({simbolo}/kg)", value=1.40 * cambio) / cambio
p_sell = st.sidebar.number_input(f"Prezzo Vendita ({simbolo}/kg)", value=2.10 * cambio) / cambio
c_ene = st.sidebar.number_input(f"Costo Energia ({simbolo}/kWh)", value=0.22 * cambio) / cambio
h_an = st.sidebar.number_input("Ore Operative/Anno", value=8000)
tol_m = st.sidebar.slider("Tolleranza Mercato (±%)", 1.0, 10.0, 6.0)

# --- INPUT COMPARAZIONE ---
col_a, col_p = st.columns(2)
with col_a:
    st.subheader(f"📊 {t['line_a']}")
    ca = st.number_input("Investimento (CAPEX) Standard", value=1500000)
    pa = st.number_input("Portata (kg/h) Standard", value=400)
    oa = st.number_input("OEE (%) Standard", value=80.0)
    sa = st.number_input("Precisione 2σ (%) Standard", value=4.5)
    scra = st.number_input("Scarto (%) Standard", value=4.0)
    ma, csa = 3.5, 0.40

with col_p:
    st.subheader(f"🚀 {t['line_b']}")
    cp = st.number_input("Investimento (CAPEX) Premium", value=2000000)
    pp = st.number_input("Portata (kg/h) Premium", value=440)
    op = st.number_input("OEE (%) Premium", value=85.0)
    sp = st.number_input("Precisione 2σ (%) Premium", value=1.5)
    scrp = st.number_input("Scarto (%) Premium", value=1.5)
    mp, csp = 2.0, 0.35

# --- CALCOLI ROI ---
ton_a = (pa * h_an * (oa/100) * (1 - scra/100)) / 1000
ton_p = (pp * h_an * (op/100) * (1 - scrp/100)) / 1000
diff_tons = ton_p - ton_a

opexa = (pa*h_an*(oa/100)*c_poly) + (pa*h_an*(oa/100)*csa*c_ene) + (ca*ma/100)
opexp = (pp*h_an*(op/100)*c_poly*(1-(tol_m-sp)/100)) + (pp*h_an*(op/100)*csp*c_ene) + (cp*mp/100)

ckga, ckgp = (opexa + (ca/10)) / (ton_a*1000), (opexp + (cp/10)) / (ton_p*1000)
marga, margp = (ton_a*1000*p_sell) - opexa, (ton_p*1000*p_sell) - opexp
dmarg = margp - marga
pbk = (cp - ca) / dmarg if dmarg > 0 else 0
p5y = (dmarg * 5) - (cp - ca)

# --- VISUALIZZAZIONE ---
st.subheader(t['tech_comp'])
data_table = {
    "Parametro": [t['annual_prod'], "OEE", "Scarto", t['cost_kg'], "Margine Annuo"],
    t['line_a']: [f"{ton_a:,.0f} T", f"{oa}%", f"{scra}%", f"{simbolo} {ckga*cambio:.3f}", f"{simbolo} {marga*cambio:,.0f}"],
    t['line_b']: [f"{ton_p:,.0f} T", f"{op}%", f"{scrp}%", f"{simbolo} {ckgp*cambio:.3f}", f"{simbolo} {margp*cambio:,.0f}"],
    "Differenza": [f"+{diff_tons:,.0f} T", f"+{op-oa}%", f"-{scra-scrp}%", f"-{simbolo} {(ckga-ckgp)*cambio:.3f}", f"+{simbolo} {dmarg*cambio:,.0f}"]
}
st.table(pd.DataFrame(data_table))

st.header(t['res_title'])
k1, k2, k3, k4 = st.columns(4)
k1.metric("Extra Margine/Anno", f"{simbolo} {dmarg*cambio:,.0f}")
k2.metric(t['extra_tons'], f"+{diff_tons:,.0f} T")
k3.metric(t['payback'], f"{pbk:.1f} Anni")
k4.metric(t['profit_5y'], f"{simbolo} {p5y*cambio:,.0f}")

# GRAFICO PAYBACK
yrs = list(range(11))
fa = [(-ca + (marga * i)) * cambio for i in yrs]
fp = [(-cp + (margp * i)) * cambio for i in yrs]
fig = go.Figure()
fig.add_trace(go.Scatter(x=yrs, y=fa, name=t['line_a'], line=dict(color='gray', dash='dot')))
fig.add_trace(go.Scatter(x=yrs, y=fp, name=t['line_b'], line=dict(color='#00CC96', width=4)))
fig.add_hline(y=0, line_color="black")
fig.update_layout(title="Analisi Cumulativa Cash Flow (Payback)", xaxis_title="Anni", yaxis_title=simbolo)
st.plotly_chart(fig, use_container_width=True)

# --- PDF GENERATOR ARRICCHITO ---
def create_rich_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(190, 10, "ROI EXTRUSION - STRATEGIC REPORT", ln=True, align='C')
    pdf.ln(10)

    # Sezione 1: Sintesi Finanziaria
    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(190, 10, " 1. FINANCIAL INDICATORS (" + simbolo + ")", ln=True, fill=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(95, 10, f"Extra Margin / Year: {simbolo} {dmarg*cambio:,.0f}", 1)
    pdf.cell(95, 10, f"Payback Period: {pbk:.1f} Years", 1, 1)
    pdf.cell(95, 10, f"5-Year Extra Profit: {simbolo} {p5y*cambio:,.0f}", 1)
    pdf.cell(95, 10, f"Extra Tons / Year: {diff_tons:,.0f} T", 1, 1)
    pdf.ln(5)

    # Sezione 2: Parametri Tecnici
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, " 2. TECHNICAL PERFORMANCE COMPARISON", ln=True, fill=True)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(60, 10, "Metric", 1); pdf.cell(65, 10, "Standard Line", 1); pdf.cell(65, 10, "Premium Line", 1, 1)
    pdf.set_font("Arial", "", 10)
    rows = [
        ("Annual Net Production", f"{ton_a:,.0f} T", f"{ton_p:,.0f} T"),
        ("Scrap Rate", f"{scra}%", f"{scrp}%"),
        ("OEE Efficiency", f"{oa}%", f"{op}%"),
        ("Production Cost/KG", f"{ckga*cambio:.3f}", f"{ckgp*cambio:.3f}")
    ]
    for r in rows:
        pdf.cell(60, 10, r[0], 1); pdf.cell(65, 10, r[1], 1); pdf.cell(65, 10, r[2], 1, 1)
    pdf.ln(5)

    # Sezione 3: Performance Drivers
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, " 3. PERFORMANCE DRIVERS & MOTIVATIONS", ln=True, fill=True)
    pdf.set_font("Arial", "", 10)
    pdf.ln(2)
    drivers = (f"- RAW MATERIAL SAVING: The 2-sigma precision of {sp}% reduces over-thickness compared to {sa}%.\n"
               f"- OPERATIONAL EFFICIENCY: Premium line OEE ({op}%) minimizes downtime and maximizes output.\n"
               f"- UNIT COST OPTIMIZATION: Saving of {simbolo} {(ckga-ckgp)*cambio:.3f} per kg produced.")
    pdf.multi_cell(190, 8, drivers)
    
    return pdf.output(dest='S').encode('latin-1', 'replace')

if st.button(t['download_pdf']):
    st.download_button("Salva Report Strategico PDF", data=create_rich_pdf(), file_name="ROI_Extrusion_Report.pdf", mime="application/pdf")
