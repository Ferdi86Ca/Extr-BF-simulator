import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import re

# --- DIZIONARIO TRADUZIONI COMPLETO ---
lang_dict = {
    "English": {
        "title": "ROI Extrusion Strategic Advisor",
        "tech_comp": "📊 Technical & Operational Comparison",
        "fin_comp": "💰 Asset Performance & Financial Yield",
        "res_title": "🏁 ROI Analysis Results",
        "download_pdf": "📩 Download FULL Strategic Report (PDF)",
        "line_a": "Standard Line",
        "line_b": "Premium Line",
        "line_c": "Fusion Line",
        "notes_label": "Meeting Notes",
        "notes_placeholder": "Enter notes...",
        "payback_label": "Payback Period (Years)",
        "crossover_title": "Cumulative Extra Profit (vs Std)",
        "t_prod": "Annual Production",
        "t_oee": "Efficiency (OEE)",
        "t_scrap": "Material Scrap",
        "t_cons": "Spec. Consumption",
        "chart_prod": "Productivity",
        "chart_prec": "Precision",
        "chart_scrap": "Scrap Recovery",
        "chart_tech": "Tech/Material Saving",
        "chart_years": "Years",
        "chart_profit": "Net Surplus",
        "cost_kg": "Production Cost per kg",
        "margin_yr": "Annual Operating Margin",
        "roi_ann": "Annualized ROI",
        "yield_5y": "5-Year Total Return (Yield)",
        "extra_5y": "5-Year Extra Profit (vs Std)",
        "factor_dist": "Savings Distribution"
    },
    "Italiano": {
        "title": "ROI Extrusion Strategic Advisor",
        "tech_comp": "📊 Comparazione Tecnica ed Operativa",
        "fin_comp": "💰 Performance Asset e Rendimento Finanziario",
        "res_title": "🏁 Risultati Analisi ROI",
        "download_pdf": "📩 Scarica Report Strategico COMPLETO (PDF)",
        "line_a": "Linea Standard",
        "line_b": "Linea Premium",
        "line_c": "Linea Fusion",
        "notes_label": "Note del Meeting / Osservazioni Strategiche",
        "notes_placeholder": "Inserisci accordi, sconti o osservazioni...",
        "payback_label": "Periodo di Payback (Anni)",
        "crossover_title": "Extra Profitto Cumulativo (vs Std)",
        "t_prod": "Produzione Annua",
        "t_oee": "Efficienza (OEE)",
        "t_scrap": "Scarto Materiale",
        "t_cons": "Consumo Specifico",
        "chart_prod": "Produttività",
        "chart_prec": "Precisione",
        "chart_scrap": "Recupero Scarti",
        "chart_tech": "Risparmio Tec/Mat",
        "chart_years": "Anni",
        "chart_profit": "Surplus Netto",
        "cost_kg": "Costo di Produzione al kg",
        "margin_yr": "Margine Operativo Annuo",
        "roi_ann": "ROI Annualizzato",
        "yield_5y": "Rendimento Totale a 5 Anni (Yield)",
        "extra_5y": "Extra Profitto 5 Anni (vs Std)",
        "factor_dist": "Distribuzione Risparmi"
    },
    "Deutsch": {
        "title": "ROI Extrusion Strategic Advisor",
        "tech_comp": "📊 Technischer Vergleich",
        "fin_comp": "💰 Finanzrendite",
        "res_title": "🏁 ROI-Ergebnisse",
        "download_pdf": "📩 PDF-Bericht herunterladen",
        "line_a": "Standard",
        "line_b": "Premium",
        "line_c": "Fusion",
        "notes_label": "Notizen",
        "notes_placeholder": "Notizen qui...",
        "payback_label": "Amortisationszeit (Jahre)",
        "crossover_title": "Zusatzgewinn",
        "t_prod": "Jährliche Produktion",
        "t_oee": "Effizienz (OEE)",
        "t_scrap": "Materialausschuss",
        "t_cons": "Spez. Verbrauch",
        "chart_prod": "Produktivität",
        "chart_prec": "Präzision",
        "chart_scrap": "Ausschuss",
        "chart_tech": "Tech/Mat Ersparnis",
        "chart_years": "Jahre",
        "chart_profit": "Nettoüberschuss",
        "cost_kg": "Produktionskosten pro kg",
        "margin_yr": "Operativer Marge",
        "roi_ann": "ROI",
        "yield_5y": "5-Jahres-Rendite",
        "extra_5y": "5-Jahres-Extraprofit",
        "factor_dist": "Einsparungen"
    },
    "Español": {
        "title": "ROI Extrusion Strategic Advisor",
        "tech_comp": "📊 Comparativa Técnica",
        "fin_comp": "💰 Rendimiento Financiero",
        "res_title": "🏁 Resultados ROI",
        "download_pdf": "📩 Descargar PDF",
        "line_a": "Estándar",
        "line_b": "Premium",
        "line_c": "Fusion",
        "notes_label": "Notas",
        "notes_placeholder": "Escribir notas...",
        "payback_label": "Periodo de Retorno (Años)",
        "crossover_title": "Beneficio Extra",
        "t_prod": "Producción Anual",
        "t_oee": "Eficiencia (OEE)",
        "t_scrap": "Desecho de Material",
        "t_cons": "Consumo Específico",
        "chart_prod": "Productividad",
        "chart_prec": "Precisión",
        "chart_scrap": "Recuperación",
        "chart_tech": "Ahorro Tec/Mat",
        "chart_years": "Años",
        "chart_profit": "Excedente Neto",
        "cost_kg": "Costo de producción por kg",
        "margin_yr": "Margen Anual",
        "roi_ann": "ROI",
        "yield_5y": "Rendimiento 5 años",
        "extra_5y": "Extra Beneficio 5 años",
        "factor_dist": "Distribución"
    }
}

st.set_page_config(page_title="ROI Advisor", layout="wide")
lingua = st.sidebar.selectbox("Language Selection", list(lang_dict.keys()), index=0)
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
        of = op 
        st.info(f"OEE Fusion: {of}%")
        sf = st.number_input("2-Sigma (%) Fusion", value=1.5)
        scrf = st.number_input("Scrap (%) Fusion", value=1.5)
        mf_fus = st.number_input("Maint. % Fusion", value=1.5)
        csf = st.number_input("kWh/kg Fusion", value=0.28)
        c_poly_f = st.number_input(f"Polymer Cost Fusion ({simbolo}/kg)", value=1.35 * cambio) / cambio

# --- CALCULATIONS LOGIC ---
def get_metrics(p, o, s, scr, cs, m, capex, cost_p, is_base=False):
    ton = (p * h_an * (o/100) * (1 - scr/100)) / 1000
    mat_eff = 1 - (tol_m - s)/100
    opex_annuo = (p * h_an * (o/100) * cost_p * mat_eff) + (p * h_an * (o/100) * cs * c_ene) + (capex * m/100)
    margin = (ton * 1000 * p_sell) - opex_annuo
    costo_kg = opex_annuo / (ton * 1000)
    payback = capex / margin if margin > 0 else 99
    
    g_prod, g_prec, g_scrap, g_tech = 0, 0, 0, 0
    if not is_base:
        g_prod = ((ton - ton_a) * 1000 * (p_sell - cost_p))
        g_prec = (p * h_an * (o/100)) * cost_p * ((sa - s)/100)
        g_scrap = (p * h_an * (o/100)) * cost_p * ((scra - scr)/100)
        g_tech = (opex_annuo_std * (ton/ton_a) - opex_annuo) 

    return ton, margin, costo_kg, payback, g_prod, g_prec, g_scrap, g_tech

# Esecuzione
ton_a, marga, ckg_a, pb_a, _, _, _, _ = get_metrics(pa, oa, sa, scra, csa, ma_std, ca, c_poly, True)
opex_annuo_std = (pa * h_an * (oa/100) * c_poly * (1 - (tol_m - sa)/100)) + (pa * h_an * (oa/100) * csa * c_ene) + (ca * ma_std/100)

ton_p, margp, ckg_p, pb_p, gp_prod, gp_prec, gp_scrap, gp_tech = get_metrics(pp, op, sp, scrp, csp, mp_pre, cp, c_poly)
if show_fusion:
    ton_f, margf, ckg_f, pb_f, gf_prod, gf_prec, gf_scrap, gf_tech = get_metrics(pf, of, sf, scrf, csf, mf_fus, cf, c_poly_f)

# --- TABLES ---
st.subheader(t['tech_comp'])
tech_data = {
    "Metric": [t['t_prod'], t['t_oee'], t['t_scrap'], t['t_cons']],
    "Standard": [f"{ton_a:,.0f} T", f"{oa}%", f"{scra}%", f"{csa} kWh/kg"],
    "Premium": [f"{ton_p:,.0f} T", f"{op}%", f"{scrp}%", f"{csp} kWh/kg"]
}
if show_fusion: tech_data["Fusion"] = [f"{ton_f:,.0f} T", f"{of}%", f"{scrf}%", f"{csf} kWh/kg"]
st.table(pd.DataFrame(tech_data))

st.subheader(t['fin_comp'])
fin_data = {
    "Indicator": [t['cost_kg'], t['margin_yr'], t['roi_ann'], t['payback_label'], t['extra_5y']],
    "Standard": [f"{simbolo} {ckg_a*cambio:.3f}", f"{simbolo} {marga*cambio:,.0f}", f"{(marga/ca)*100:.1f}%", f"{pb_a:.2f}", "-"],
    "Premium": [f"{simbolo} {ckg_p*cambio:.3f}", f"{simbolo} {margp*cambio:,.0f}", f"{(margp/cp)*100:.1f}%", f"{pb_p:.2f}", f"{simbolo} {(margp-marga)*5*cambio:,.0f}"]
}
if show_fusion:
    fin_data["Fusion"] = [f"{simbolo} {ckg_f*cambio:.3f}", f"{simbolo} {margf*cambio:,.0f}", f"{(margf/cf)*100:.1f}%", f"{pb_f:.2f}", f"{simbolo} {(margf-marga)*5*cambio:,.0f}"]
st.table(pd.DataFrame(fin_data))

# --- CHARTS ---
st.header(t['res_title'])
c1, c2 = st.columns(2)
with c1:
    # Grafico Payback Comparison
    pb_names = [t['line_a'], t['line_b']]
    pb_values = [pb_a, pb_p]
    if show_fusion:
        pb_names.append(t['line_c'])
        pb_values.append(pb_f)
    
    fig_pb = go.Figure(go.Bar(y=pb_names, x=pb_values, orientation='h', marker_color=['#636EFA', '#00CC96', '#AB63FA']))
    fig_pb.update_layout(title=t['payback_label'], xaxis_title=t['chart_years'], yaxis={'autorange': "reversed"})
    st.plotly_chart(fig_pb, use_container_width=True)

with c2:
    yrs = [i/4 for i in range(41)]
    fig_cross = go.Figure()
    fig_cross.add_trace(go.Scatter(x=yrs, y=[(-(cp-ca)+(margp-marga)*y)*cambio for y in yrs], name=t['line_b']))
    if show_fusion:
        fig_cross.add_trace(go.Scatter(x=yrs, y=[(-(cf-ca)+(margf-marga)*y)*cambio for y in yrs], name=t['line_c']))
    fig_cross.add_hline(y=0, line_dash="dash", line_color="red")
    fig_cross.update_layout(title=t['crossover_title'], xaxis_title=t['chart_years'], yaxis_title=t['chart_profit'])
    st.plotly_chart(fig_cross, use_container_width=True)



st.divider()
notes = st.text_area(t['notes_label'], placeholder=t['notes_placeholder'], height=100)
