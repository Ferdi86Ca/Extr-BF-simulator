import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from fpdf import FPDF
import tempfile
import os
import re

# Funzione per rimuovere emoji e caratteri speciali non compatibili con il PDF standard
def clean_text(text):
    return re.sub(r'[^\x00-\x7F]+', '', str(text))

# 1. DIZIONARIO TRADUZIONI (5 Lingue)
lang_dict = {
    "Italiano": {
        "title": "ROI Extrusion Strategic Advisor",
        "tech_comp": "📊 Comparazione Tecnica ed Operativa",
        "fin_comp": "💰 Performance Asset e Rendimento Finanziario",
        "res_title": "🏁 Risultati Analisi ROI",
        "download_pdf": "📩 Scarica Report Strategico COMPLETO (PDF)",
        "annual_prod": "Produzione Annua Netta",
        "margin_yr": "Margine Operativo Annuo",
        "roi_ann": "ROI Annualizzato",
        "yield_5y": "Rendimento Totale a 5 Anni (Yield)",
        "factor_dist": "Distribuzione Risparmi",
        "line_a": "Linea Standard",
        "line_b": "Linea Premium",
        "line_c": "Linea Fusion",
        "payback_months": "Mesi per rientro Extra CAPEX",
        "crossover_title": "Extra Profitto Cumulativo (vs Std)"
    },
    "English": {
        "title": "ROI Extrusion Strategic Advisor",
        "tech_comp": "📊 Technical & Operational Comparison",
        "fin_comp": "💰 Asset Performance & Financial Yield",
        "res_title": "🏁 ROI Analysis Results",
        "download_pdf": "📩 Download FULL Strategic Report (PDF)",
        "annual_prod": "Annual Net Production",
        "margin_yr": "Annual Operating Margin",
        "roi_ann": "Annualized ROI",
        "yield_5y": "5-Year Total Return (Yield)",
        "factor_dist": "Savings Distribution",
        "line_a": "Standard Line",
        "line_b": "Premium Line",
        "line_c": "Fusion Line",
        "payback_months": "Months to Payback Extra CAPEX",
        "crossover_title": "Cumulative Extra Profit (vs Std)"
    },
    "Deutsch": {
        "title": "ROI Extrusion Strategic Advisor",
        "tech_comp": "📊 Technischer & Operativer Vergleich",
        "fin_comp": "💰 Asset-Performance & Finanzrendite",
        "res_title": "🏁 ROI-Analyseergebnisse",
        "download_pdf": "📩 Strategiebericht (PDF) herunterladen",
        "annual_prod": "Jährliche Nettoproduktion",
        "margin_yr": "Jährliche operativer Marge",
        "roi_ann": "Annualisierter ROI",
        "yield_5y": "5-Jahres-Rendite",
        "factor_dist": "Einsparungsverteilung",
        "line_a": "Standard-Linie",
        "line_b": "Premium-Linie",
        "line_c": "Fusion-Linie",
        "payback_months": "Amortisationszeit (Extra CAPEX)",
        "crossover_title": "Kumulierter Zusatzgewinn (vs. Std.)"
    },
    "Español": {
        "title": "ROI Extrusion Strategic Advisor",
        "tech_comp": "📊 Comparativa Técnica y Operativa",
        "fin_comp": "💰 Rendimiento del Activo",
        "res_title": "🏁 Resultados ROI",
        "download_pdf": "📩 Descargar Informe (PDF)",
        "annual_prod": "Producción Neta Anual",
        "margin_yr": "Margen Operativo Anual",
        "roi_ann": "ROI Anualizado",
        "yield_5y": "Rendimento Total a 5 años",
        "factor_dist": "Distribución de Ahorros",
        "line_a": "Línea Estándar",
        "line_b": "Línea Premium",
        "line_c": "Línea Fusion",
        "payback_months": "Meses para amortizar Extra CAPEX",
        "crossover_title": "Beneficio Extra Acumulado (vs Std)"
    },
    "العربية": {
        "title": "مستشار استراتيجية عائد الاستثمار في البثق",
        "tech_comp": "المقارنة الفنية والتشغيلية",
        "fin_comp": "أداء الأصول والعائد المالي",
        "res_title": "نتائج تحليل عائد الاستثمار (ROI)",
        "download_pdf": "تحميل التقرير الاستراتيجي الكامل (PDF)",
        "annual_prod": "الإنتاج السنوي الصافي",
        "margin_yr": "هامش التشغيل السنوي",
        "roi_ann": "عائد الاستثمار السنوي",
        "yield_5y": "إجمالي العائد لمدة 5 سنوات",
        "factor_dist": "توزيع محركات الربح",
        "line_a": "الخط القياسي",
        "line_b": "الخط المتميز",
        "line_c": "Fusion الخط",
        "payback_months": "أشهر لاسترداد الإنفاق الرأسمالي الإضافي",
        "crossover_title": "إجمالي الربح الإضافي"
    }
}

st.set_page_config(page_title="ROI Advisor", layout="wide")
lingua = st.sidebar.selectbox("Language / Lingua / Sprache / Idioma / اللغة", ["Italiano", "English", "Deutsch", "Español", "العربية"])
t = lang_dict[lingua]
st.title(t['title'])

# --- SIDEBAR: MARKET SETTINGS ---
st.sidebar.header("🌍 Market Settings")
valuta_sel = st.sidebar.radio("Currency", ["EUR", "USD"])
cambio = 1.0; simbolo = "EUR"
if valuta_sel == "USD":
    cambio = st.sidebar.number_input("Exchange Rate (1€ = X $)", value=1.08)
    simbolo = "USD"

c_poly = st.sidebar.number_input(f"Polymer Cost ({simbolo}/kg)", value=1.50 * cambio) / cambio
p_sell = st.sidebar.number_input(f"Selling Price ({simbolo}/kg)", value=2.00 * cambio) / cambio
c_ene = st.sidebar.number_input(f"Energy Cost ({simbolo}/kWh)", value=0.22 * cambio) / cambio
h_an = st.sidebar.number_input("Hours/Year", value=7500)
tol_m = st.sidebar.slider("Market Tol. (±%)", 1.0, 10.0, 6.0)

# Attivazione Linea Fusion
show_fusion = st.sidebar.checkbox("Show Fusion Line", value=False)

# --- INPUT COMPARISON ---
cols = st.columns(3 if show_fusion else 2)
with cols[0]:
    st.subheader(f"⚪ {t['line_a']}")
    ca = st.number_input("CAPEX Standard", value=1500000)
    pa = st.number_input("Output (kg/h) Std", value=400)
    oa = st.number_input("OEE (%) Std", value=83.0)
    sa = st.number_input("2-Sigma (%) Std", value=3.5)
    scra = st.number_input("Scrap (%) Std", value=2.0)
    ma_std = st.number_input("Maint. % Std", value=2.5)
    csa = st.number_input("kWh/kg Std", value=0.40)

with cols[1]:
    st.subheader(f"💎 {t['line_b']}")
    cp = st.number_input("CAPEX Premium", value=2000000)
    pp = st.number_input("Output (kg/h) Prem", value=440)
    op = st.number_input("OEE (%) Prem", value=87.0)
    sp = st.number_input("2-Sigma (%) Prem", value=1.5)
    scrp = st.number_input("Scrap (%) Prem", value=1.5)
    mp_pre = st.number_input("Maint. % Prem", value=1.5)
    csp = st.number_input("kWh/kg Prem", value=0.35)

if show_fusion:
    with cols[2]:
        st.subheader(f"🌀 {t['line_c']}")
        cf = st.number_input("CAPEX Fusion", value=2200000)
        pf = st.number_input("Output (kg/h) Fusion", value=440)
        of = st.number_input("OEE (%) Fusion", value=88.0)
        sf = st.number_input("2-Sigma (%) Fusion", value=1.5)
        scrf = st.number_input("Scrap (%) Fusion", value=1.5)
        mf_fus = st.number_input("Maint. % Fusion", value=1.5)
        csf = st.number_input("kWh/kg Fusion", value=0.28)
        c_poly_f = st.number_input(f"Polymer Cost Fusion ({simbolo}/kg)", value=1.35 * cambio) / cambio

# --- CALCULATIONS & LOGIC ---
# 1. Calcoli Base (Standard)
ton_a = (pa * h_an * (oa/100) * (1 - scra/100)) / 1000
marga = (ton_a*1000*p_sell) - ((pa*h_an*(oa/100)*c_poly) + (pa*h_an*(oa/100)*csa*c_ene) + (ca*ma_std/100))

# Funzione Helper per calcolare guadagni e margini
def calc_line_performance(p, o, s, scr, cs, m, capex, cost_p):
    ton = (p * h_an * (o/100) * (1 - scr/100)) / 1000
    g_prod = (ton - ton_a) * 1000 * (p_sell - cost_p)
    g_prec = (p * h_an * (o/100)) * cost_p * ((tol_m - s)/100 - (tol_m - sa)/100)
    g_scrap = (p * h_an * (o/100)) * cost_p * ((scra - scr)/100)
    g_ene = (pa * h_an * (oa/100)) * (csa - cs) * c_ene
    g_maint = (ca * ma_std/100) - (capex * m/100)
    g_mat_saving = (ton * 1000) * (c_poly - cost_p) if cost_p < c_poly else 0
    total_margin = marga + (g_prod + g_prec + g_scrap + g_ene + g_maint + g_mat_saving)
    return ton, total_margin, g_prod, g_prec, g_scrap, (g_ene + g_maint + g_mat_saving)

# 2. Calcoli Premium
ton_p, margp, gp_prod, gp_prec, gp_scrap, gp_tech = calc_line_performance(pp, op, sp, scrp, csp, mp_pre, cp, c_poly)

# 3. Calcoli Fusion
if show_fusion:
    ton_f, margf, gf_prod, gf_prec, gf_scrap, gf_tech = calc_line_performance(pf, of, sf, scrf, csf, mf_fus, cf, c_poly_f)

# --- TABLES ---
st.subheader(t['tech_comp'])
tech_data = {
    "Metric": ["Real Output", "Total Annual Prod.", "Efficiency (OEE)", "Material Scrap", "Specific Cons.", "Maintenance"],
    "Standard": [f"{pa} kg/h", f"{ton_a:,.0f} T", f"{oa}%", f"{scra}%", f"{csa} kWh/kg", f"{ma_std}%"],
    "Premium": [f"{pp} kg/h", f"{ton_p:,.0f} T", f"{op}%", f"{scrp}%", f"{csp} kWh/kg", f"{mp_pre}%"]
}
if show_fusion:
    tech_data["Fusion"] = [f"{pf} kg/h", f"{ton_f:,.0f} T", f"{of}%", f"{scrf}%", f"{csf} kWh/kg", f"{mf_fus}%"]
st.table(pd.DataFrame(tech_data))

st.subheader(t['fin_comp'])
fin_data = {
    "Indicator": [t['margin_yr'], t['roi_ann'], t['yield_5y']],
    "Standard": [f"{simbolo} {marga*cambio:,.0f}", f"{(marga/ca)*100:.1f}%", f"{(marga*5/ca)*100:.1f}%"],
    "Premium": [f"{simbolo} {margp*cambio:,.0f}", f"{(margp/cp)*100:.1f}%", f"{(margp*5/cp)*100:.1f}%"]
}
if show_fusion:
    fin_data["Fusion"] = [f"{simbolo} {margf*cambio:,.0f}", f"{(margf/cf)*100:.1f}%", f"{(margf*5/cf)*100:.1f}%"]
st.table(pd.DataFrame(fin_data))

# Metriche Payback
payback_p = ((cp - ca) / (margp - marga)) * 12 if (margp - marga) > 0 else 0
st.metric(label=f"⭐ {t['payback_months']} (Premium vs Std)", value=f"{payback_p:.1f} Months")

if show_fusion:
    payback_f = ((cf - ca) / (margf - marga)) * 12 if (margf - marga) > 0 else 0
    st.metric(label=f"🌀 {t['payback_months']} (Fusion vs Std)", value=f"{payback_f:.1f} Months")

# --- CHARTS SECTION ---
st.header(t['res_title'])
c1, c2 = st.columns(2)

with c1:
    labels = ['Produttività', 'Precisione', 'Recupero Scarti', 'Efficienza Tecnica/Materiale']
    if not show_fusion:
        fig_pie = go.Figure(data=[go.Pie(labels=labels, values=[max(0,gp_prod), max(0,gp_prec), max(0,gp_scrap), max(0,gp_tech)], hole=.4)])
        fig_pie.update_layout(title=f"{t['factor_dist']} (Premium vs Std)")
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        sc1, sc2 = st.columns(2)
        with sc1:
            f1 = go.Figure(data=[go.Pie(labels=labels, values=[max(0,gp_prod), max(0,gp_prec), max(0,gp_scrap), max(0,gp_tech)], hole=.4)])
            f1.update_layout(title="Premium vs Std", showlegend=False)
            st.plotly_chart(f1, use_container_width=True)
        with sc2:
            f2 = go.Figure(data=[go.Pie(labels=labels, values=[max(0,gf_prod), max(0,gf_prec), max(0,gf_scrap), max(0,gf_tech)], hole=.4)])
            f2.update_layout(title="Fusion vs Std", showlegend=False)
            st.plotly_chart(f2, use_container_width=True)

with c2:
    yrs = [i/4 for i in range(41)]
    fig_cross = go.Figure()
    fig_cross.add_trace(go.Scatter(x=yrs, y=[(- (cp - ca) + (margp - marga) * y) * cambio for y in yrs], name="Premium vs Std", line=dict(color='#00CC96', width=4)))
    if show_fusion:
        fig_cross.add_trace(go.Scatter(x=yrs, y=[(- (cf - ca) + (margf - marga) * y) * cambio for y in yrs], name="Fusion vs Std", line=dict(color='#AB63FA', width=4)))
    fig_cross.add_hline(y=0, line_dash="dash", line_color="red")
    fig_cross.update_layout(title=t['crossover_title'], xaxis_title="Anni", paper_bgcolor='white', plot_bgcolor='white')
    st.plotly_chart(fig_cross, use_container_width=True)

st.divider()
meeting_notes = st.text_area(t['notes_label'], placeholder=t['notes_placeholder'], height=150)

if st.button(t['download_pdf']):
    st.info("Generazione report in corso...")
