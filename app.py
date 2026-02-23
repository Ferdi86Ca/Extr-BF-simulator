import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from fpdf import FPDF
import tempfile
import os
import re

# Funzione per rimuovere emoji e caratteri speciali per compatibilità PDF
def clean_text(text):
    return re.sub(r'[^\x00-\x7F]+', '', str(text))

# 1. DIZIONARIO TRADUZIONI COMPLETO
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
        "notes_label": "Note del Meeting / Osservazioni Strategiche",
        "notes_placeholder": "Inserisci accordi, sconti o osservazioni...",
        "payback_months": "Mesi per rientro Extra CAPEX",
        "crossover_title": "Extra Profitto Cumulativo (vs Std)",
        "t_prod": "Produzione Annua",
        "t_oee": "Efficienza (OEE)",
        "t_scrap": "Scarto Materiale",
        "t_cons": "Consumo Specifico"
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
        "notes_label": "Meeting Notes",
        "notes_placeholder": "Enter notes...",
        "payback_months": "Months to Payback Extra CAPEX",
        "crossover_title": "Cumulative Extra Profit (vs Std)",
        "t_prod": "Annual Production",
        "t_oee": "Efficiency (OEE)",
        "t_scrap": "Material Scrap",
        "t_cons": "Spec. Consumption"
    },
    "Deutsch": {
        "title": "ROI Extrusion Strategic Advisor",
        "tech_comp": "📊 Technischer Vergleich",
        "fin_comp": "💰 Finanzrendite",
        "res_title": "🏁 ROI-Ergebnisse",
        "download_pdf": "📩 PDF-Bericht herunterladen",
        "annual_prod": "Nettoproduktion",
        "margin_yr": "Operativer Marge",
        "roi_ann": "ROI",
        "yield_5y": "5-Jahres-Rendite",
        "factor_dist": "Einsparungen",
        "line_a": "Standard",
        "line_b": "Premium",
        "line_c": "Fusion",
        "notes_label": "Notizen",
        "notes_placeholder": "Notizen qui...",
        "payback_months": "Amortisation (Monate)",
        "crossover_title": "Zusatzgewinn",
        "t_prod": "Jährliche Produktion",
        "t_oee": "Effizienz (OEE)",
        "t_scrap": "Materialausschuss",
        "t_cons": "Spez. Verbrauch"
    },
    "Español": {
        "title": "ROI Extrusion Strategic Advisor",
        "tech_comp": "📊 Comparativa Técnica",
        "fin_comp": "💰 Rendimiento Financiero",
        "res_title": "🏁 Resultados ROI",
        "download_pdf": "📩 Descargar PDF",
        "annual_prod": "Producción Neta",
        "margin_yr": "Margen Anual",
        "roi_ann": "ROI",
        "yield_5y": "Rendimiento 5 años",
        "factor_dist": "Distribución",
        "line_a": "Estándar",
        "line_b": "Premium",
        "line_c": "Fusion",
        "notes_label": "Notas",
        "notes_placeholder": "Escribir notas...",
        "payback_months": "Meses retorno",
        "crossover_title": "Beneficio Extra",
        "t_prod": "Producción Anual",
        "t_oee": "Eficiencia (OEE)",
        "t_scrap": "Desecho de Material",
        "t_cons": "Consumo Específico"
    },
    "العربية": {
        "title": "مستشار استراتيجية عائد الاستثمار",
        "tech_comp": "المقارنة الفنية والتشغيلية",
        "fin_comp": "أداء الأصول والعائد المالي",
        "res_title": "نتائج تحليل عائد الاستثمار",
        "download_pdf": "تحميل التقرير (PDF)",
        "annual_prod": "الإنتاج السنوي",
        "margin_yr": "هامش التشغيل",
        "roi_ann": "عائد الاستثمار",
        "yield_5y": "إجمالي العائد 5 سنوات",
        "factor_dist": "توزيع محركات الربح",
        "line_a": "الخط القياسي",
        "line_b": "الخط المتميز",
        "line_c": "خط Fusion",
        "notes_label": "ملاحظات",
        "notes_placeholder": "أدخل الملاحظات هنا...",
        "payback_months": "أشهر الاسترداد",
        "crossover_title": "إجمالي الربح الإضافي",
        "t_prod": "الإنتاج السنوي",
        "t_oee": "كفاءة المعدات",
        "t_scrap": "خردة المواد",
        "t_cons": "استهلاك الطاقة"
    }
}

st.set_page_config(page_title="ROI Advisor", layout="wide")
lingua = st.sidebar.selectbox("Language / Lingua / Sprache / Idioma / اللغة", list(lang_dict.keys()))
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
        of = op # OEE uguale a Premium
        st.info(f"OEE Fusion: {of}%")
        sf = st.number_input("2-Sigma (%) Fusion", value=1.5)
        scrf = st.number_input("Scrap (%) Fusion", value=1.5)
        mf_fus = st.number_input("Maint. % Fusion", value=1.5)
        csf = st.number_input("kWh/kg Fusion", value=0.28)
        c_poly_f = st.number_input(f"Polymer Cost Fusion ({simbolo}/kg)", value=1.35 * cambio) / cambio

# --- CALCULATIONS ---
ton_a = (pa * h_an * (oa/100) * (1 - scra/100)) / 1000
mat_eff_a = 1 - (tol_m - sa)/100
marga = (ton_a * 1000 * p_sell) - (pa * h_an * (oa/100) * c_poly * mat_eff_a) - (pa * h_an * (oa/100) * csa * c_ene) - (ca * ma_std/100)

def get_performance_vs_std(p, o, s, scr, cs, m, capex, cost_p):
    ton = (p * h_an * (o/100) * (1 - scr/100)) / 1000
    mat_eff = 1 - (tol_m - s)/100
    margin = (ton * 1000 * p_sell) - (p * h_an * (o/100) * cost_p * mat_eff) - (p * h_an * (o/100) * cs * c_ene) - (capex * m/100)
    g_prod = ((ton - ton_a) * 1000 * (p_sell - cost_p))
    g_prec = (p * h_an * (o/100)) * cost_p * ((sa - s)/100)
    g_scrap = (p * h_an * (o/100)) * cost_p * ((scra - scr)/100)
    g_tech_energy = (pa * h_an * (oa/100) * csa * c_ene - p * h_an * (o/100) * cs * c_ene)
    g_maint = (ca * ma_std/100 - capex * m/100)
    g_mat_base = (ton * 1000) * (c_poly - cost_p) if cost_p < c_poly else 0
    return ton, margin, g_prod, g_prec, g_scrap, (g_tech_energy + g_maint + g_mat_base)

ton_p, margp, gp_prod, gp_prec, gp_scrap, gp_tech = get_performance_vs_std(pp, op, sp, scrp, csp, mp_pre, cp, c_poly)

if show_fusion:
    ton_f, margf, gf_prod, gf_prec, gf_scrap, gf_tech = get_performance_vs_std(pf, of, sf, scrf, csf, mf_fus, cf, c_poly_f)

# --- TABLES ---
st.subheader(t['tech_comp'])
tech_data = {
    "Metric": [t['t_prod'], t['t_oee'], t['t_scrap'], t['t_cons']],
    "Standard": [f"{ton_a:,.0f} T", f"{oa}%", f"{scra}%", f"{csa} kWh/kg"],
    "Premium": [f"{ton_p:,.0f} T", f"{op}%", f"{scrp}%", f"{csp} kWh/kg"]
}
if show_fusion:
    tech_data["Fusion"] = [f"{ton_f:,.0f} T", f"{of}%", f"{scrf}%", f"{csf} kWh/kg"]
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

# --- CHARTS ---
st.header(t['res_title'])
c1, c2 = st.columns(2)
with c1:
    labels = ['Produttività', 'Precisione', 'Scarti', 'Tech/Material Saving']
    if not show_fusion:
        fig = go.Figure(data=[go.Pie(labels=labels, values=[max(0.1, gp_prod), max(0.1, gp_prec), max(0.1, gp_scrap), max(0.1, gp_tech)], hole=.4)])
        fig.update_layout(title=f"{t['factor_dist']} (Premium vs Std)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        sc1, sc2 = st.columns(2)
        with sc1:
            f1 = go.Figure(data=[go.Pie(labels=labels, values=[max(0.1, gp_prod), max(0.1, gp_prec), max(0.1, gp_scrap), max(0.1, gp_tech)], hole=.4)])
            f1.update_layout(title="Premium vs Std", showlegend=False); st.plotly_chart(f1, use_container_width=True)
        with sc2:
            f2 = go.Figure(data=[go.Pie(labels=labels, values=[max(0.1, gf_prod), max(0.1, gf_prec), max(0.1, gf_scrap), max(0.1, gf_tech)], hole=.4)])
            f2.update_layout(title="Fusion vs Std", showlegend=False); st.plotly_chart(f2, use_container_width=True)

with c2:
    yrs = [i/4 for i in range(41)]
    fig_cross = go.Figure()
    fig_cross.add_trace(go.Scatter(x=yrs, y=[(-(cp-ca)+(margp-marga)*y)*cambio for y in yrs], name="Premium vs Std", line=dict(color='#00CC96')))
    if show_fusion:
        fig_cross.add_trace(go.Scatter(x=yrs, y=[(-(cf-ca)+(margf-marga)*y)*cambio for y in yrs], name="Fusion vs Std", line=dict(color='#AB63FA')))
    fig_cross.add_hline(y=0, line_dash="dash", line_color="red")
    fig_cross.update_layout(title=t['crossover_title'], xaxis_title="Anni")
    st.plotly_chart(fig_cross, use_container_width=True)

st.divider()
notes = st.text_area(t['notes_label'], placeholder=t['notes_placeholder'], height=100)

if st.button(t['download_pdf']):
    st.info("Generazione report in corso...")
