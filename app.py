import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from fpdf import FPDF

# --- TRADUZIONI ---
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
        "exchange_rate": "Exchange Rate (1€ = X $)"
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
        "exchange_rate": "Tasso di Cambio (1€ = X $)"
    }
}

st.set_page_config(page_title="ROI Extrusion", layout="wide")
lingua = st.sidebar.selectbox("Language / Lingua", ["Italiano", "English"])
t = lang_dict[lingua]

st.title(t['title'])

# --- SIDEBAR: PARAMETRI DI MERCATO ---
st.sidebar.header("🌍 Market & General Settings")
valuta_sel = st.sidebar.radio("Currency / Valuta", ["EUR", "USD"])
cambio = 1.0; simbolo = "EUR"
if valuta_sel == "USD":
    cambio = st.sidebar.number_input(t['exchange_rate'], value=1.08)
    simbolo = "USD"

c_poly = st.sidebar.number_input(f"Costo Polimero ({simbolo}/kg)", value=1.40 * cambio) / cambio
p_sell = st.sidebar.number_input(f"Prezzo Vendita ({simbolo}/kg)", value=2.10 * cambio) / cambio
c_ene = st.sidebar.number_input(f"Costo Energia ({simbolo}/kWh)", value=0.22 * cambio) / cambio
h_an = st.sidebar.number_input("Ore Operative/Anno", value=8000)
tol_m = st.sidebar.slider("Market Tolerance (±%)", 1.0, 10.0, 6.0)

# --- INPUT LINEE (Parametri Richiesti) ---
col_a, col_p = st.columns(2)

with col_a:
    st.subheader(f"⚪ {t['line_a']}")
    ca = st.number_input("CAPEX Standard", value=1500000)
    pa = st.number_input("Portata (kg/h) Standard", value=400)
    oa = st.number_input("OEE (%) Standard", value=83.0, key="oa_in")
    sa = st.number_input("2-Sigma (%) Standard", value=3.5, key="sa_in")
    scra = st.number_input("Scrap (%) Standard", value=2.0, key="scra_in")
    ma, csa = 3.5, 0.40

with col_p:
    st.subheader(f"💎 {t['line_b']}")
    cp = st.number_input("CAPEX Premium", value=2000000)
    pp = st.number_input("Portata (kg/h) Premium", value=440)
    op = st.number_input("OEE (%) Premium", value=87.0, key="op_in")
    sp = st.number_input("2-Sigma (%) Premium", value=1.5, key="sp_in")
    scrp = st.number_input("Scrap (%) Premium", value=1.5, key="scrp_in")
    mp, csp = 2.0, 0.35

# --- CALCOLI ---
ton_a = (pa * h_an * (oa/100) * (1 - scra/100)) / 1000
ton_p = (pp * h_an * (op/100) * (1 - scrp/100)) / 1000
diff_tons = ton_p - ton_a

# OPEX calcolato con risparmio materia prima grazie alla precisione 2-sigma
opexa = (pa*h_an*(oa/100)*c_poly) + (pa*h_an*(oa/100)*csa*c_ene) + (ca*ma/100)
opexp = (pp*h_an*(op/100)*c_poly*(1-(tol_m-sp)/100)) + (pp*h_an*(op/100)*csp*c_ene) + (cp*mp/100)

ckga = (opexa + (ca/10)) / (ton_a*1000) if ton_a > 0 else 0
ckgp = (opexp + (cp/10)) / (ton_p*1000) if ton_p > 0 else 0
marga = (ton_a*1000*p_sell) - opexa
margp = (ton_p*1000*p_sell) - opexp
dmarg = margp - marga
pbk = (cp - ca) / dmarg if dmarg > 0 else 0
p5y = (dmarg * 5) - (cp - ca)

# --- TABELLA UI ---
st.subheader(t['tech_comp'])
diff_ckg = (ckga - ckgp) * cambio
df_visual = pd.DataFrame({
    "Parameter": [t['annual_prod'], "OEE Efficiency", "Scrap Rate", "2-Sigma Precision", t['cost_kg'], t['margin_yr']],
    t['line_a']: [f"{ton_a:,.0f} T", f"{oa}%", f"{scra}%", f"{sa}%", f"{simbolo} {ckga*cambio:.3f}", f"{simbolo} {marga*cambio:,.0f}"],
    t['line_b']: [f"{ton_p:,.0f} T", f"{op}%", f"{scrp}%", f"{sp}%", f"{simbolo} {ckgp*cambio:.3f}", f"{simbolo} {margp*cambio:,.0f}"],
    "Analysis": [f"📈 +{diff_tons:,.0f} T", f"✅ +{op-oa}%", f"📉 -{scra-scrp}%", f"🎯 {sp-sa}%", f"💸 -{simbolo} {diff_ckg:.3f}", f"🔥 +{simbolo} {dmarg*cambio:,.0f}"]
})
st.table(df_visual)

# --- KPI E GRAFICO ---
st.header(t['res_title'])
k1, k2, k3, k4 = st.columns(4)
k1.metric(t['margin_yr'] + " Extra", f"{simbolo} {dmarg*cambio:,.0f}")
k2.metric(t['extra_tons'], f"+{diff_tons:,.0f} T")
k3.metric(t['payback'], f"{pbk:.1f} Yrs")
k4.metric(t['profit_5y'], f"{simbolo} {p5y*cambio:,.0f}")

yrs = list(range(11))
fa = [(-ca + (marga * i)) * cambio for i in yrs]
fp = [(-cp + (margp * i)) * cambio for i in yrs]
fig = go.Figure()
fig.add_trace(go.Scatter(x=yrs, y=fa, name=t['line_a'], line=dict(color='gray', dash='dot')))
fig.add_trace(go.Scatter(x=yrs, y=fp, name=t['line_b'], line=dict(color='#00CC96', width=4)))
fig.add_hline(y=0, line_color="black")
fig.update_layout(title="Payback Strategy: Cumulative Cash Flow", xaxis_title="Years", yaxis_title=simbolo)
st.plotly_chart(fig, use_container_width=True)

# --- SEZIONE NOTE ---
st.divider()
user_notes = st.text_area("Note del Meeting / Meeting Notes", placeholder="Scrivi qui gli accordi presi o le osservazioni del cliente...")

# --- PDF GENERATOR ---
def create_full_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    pdf.cell(190, 15, "ROI EXTRUSION - STRATEGIC REPORT", ln=True, align='C')
    pdf.set_font("Arial", "I", 10)
    pdf.cell(190, 5, "Simulated Scenarios: Standard vs Premium Line", ln=True, align='C')
    pdf.ln(10)
    
    # Sezione 1: Mercato
    pdf.set_font("Arial", "B", 12); pdf.set_fill_color(240, 240, 240)
    pdf.cell(190, 10, " 1. MARKET DATA & ASSUMPTIONS", ln=True, fill=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(95, 8, f"Resin Cost: {c_poly*cambio:,.2f} {simbolo}/kg", 1); pdf.cell(95, 8, f"Selling Price: {p_sell*cambio:,.2f} {simbolo}/kg", 1, 1)
    pdf.cell(95, 8, f"Energy Cost: {c_ene*cambio:,.2f} {simbolo}/kWh", 1); pdf.cell(95, 8, f"Operating Hours: {h_an} h/y", 1, 1)
    pdf.ln(5)

    # Sezione 2: Tecnica
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, " 2. TECHNICAL SPECIFICATIONS", ln=True, fill=True)
    pdf.set_font("Arial", "B", 9)
    pdf.cell(60, 8, "Metric", 1); pdf.cell(65, 8, "STANDARD LINE", 1); pdf.cell(65, 8, "PREMIUM LINE", 1, 1)
    pdf.set_font("Arial", "", 9)
    pdf.cell(60, 8, "CAPEX", 1); pdf.cell(65, 8, f"{ca*cambio:,.0f} {simbolo}", 1); pdf.cell(65, 8, f"{cp*cambio:,.0f} {simbolo}", 1, 1)
    pdf.cell(60, 8, "OEE", 1); pdf.cell(65, 8, f"{oa}%", 1); pdf.cell(65, 8, f"{op}%", 1, 1)
    pdf.cell(60, 8, "Scrap", 1); pdf.cell(65, 8, f"{scra}%", 1); pdf.cell(65, 8, f"{scrp}%", 1, 1)
    pdf.cell(60, 8, "2-Sigma", 1); pdf.cell(65, 8, f"{sa}%", 1); pdf.cell(65, 8, f"{sp}%", 1, 1)
    pdf.ln(5)

    # Sezione 3: ROI
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, " 3. ROI & PERFORMANCE", ln=True, fill=True)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(95, 8, "Indicator", 1); pdf.cell(95, 8, "Value", 1, 1)
    pdf.set_font("Arial", "", 10)
    pdf.cell(95, 8, "Extra Margin / Year", 1); pdf.cell(95, 8, f"{dmarg*cambio:,.0f} {simbolo}", 1, 1)
    pdf.cell(95, 8, "Payback Period", 1); pdf.cell(95, 8, f"{pbk:.1f} Years", 1, 1)
    pdf.cell(95, 8, "5-Year Profit Gain", 1); pdf.cell(95, 8, f"{p5y*cambio:,.0f} {simbolo}", 1, 1)
    pdf.ln(5)

    # Sezione 4: Note
    if user_notes:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(190, 10, " 4. MEETING NOTES", ln=True, fill=True)
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(190, 8, user_notes, 1)
    
    return pdf.output(dest='S').encode('latin-1', 'replace')

if st.button(t['download_pdf']):
    st.download_button("Download Full Report PDF", data=create_full_pdf(), file_name="ROI_Extrusion_Final.pdf", mime="application/pdf")
