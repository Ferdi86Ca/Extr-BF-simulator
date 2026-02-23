import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# --- DIZIONARIO TRADUZIONI COMPLETO ---
lang_dict = {
    "English": {
        "title": "ROI Extrusion Strategic Advisor",
        "tech_comp": "📊 Technical & Operational Comparison",
        "fin_comp": "💰 Asset Performance & Financial Yield",
        "res_title": "🏁 ROI Analysis Results",
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
        "chart_years": "Years",
        "chart_profit": "Net Surplus",
        "cost_kg": "Unit Cost (per kg)",
        "margin_yr": "Annual Op. Margin",
        "roi_ann": "Annualized ROI",
        "extra_5y": "5-Year Extra Profit (vs Std)",
        "market_settings": "Market Settings"
    },
    "Italiano": {
        "title": "ROI Extrusion Strategic Advisor",
        "tech_comp": "📊 Comparazione Tecnica ed Operativa",
        "fin_comp": "💰 Performance Asset e Rendimento Finanziario",
        "res_title": "🏁 Risultati Analisi ROI",
        "line_a": "Linea Standard",
        "line_b": "Linea Premium",
        "line_c": "Linea Fusion",
        "notes_label": "Note del Meeting",
        "notes_placeholder": "Inserisci note...",
        "payback_label": "Periodo di Payback (Anni)",
        "crossover_title": "Extra Profitto Cumulativo (vs Std)",
        "t_prod": "Produzione Annua",
        "t_oee": "Efficienza (OEE)",
        "t_scrap": "Scarto Materiale",
        "t_cons": "Consumo Specifico",
        "chart_years": "Anni",
        "chart_profit": "Surplus Netto",
        "cost_kg": "Costo Unitario (al kg)",
        "margin_yr": "Margine Operativo Annuo",
        "roi_ann": "ROI Annualizzato",
        "extra_5y": "Extra Profitto 5 Anni (vs Std)",
        "market_settings": "Impostazioni Mercato"
    },
    "Deutsch": {
        "title": "ROI Extrusion Strategic Advisor",
        "tech_comp": "📊 Technischer Vergleich",
        "fin_comp": "💰 Finanzielle Performance",
        "res_title": "🏁 ROI-Ergebnisse",
        "line_a": "Standard",
        "line_b": "Premium",
        "line_c": "Fusion",
        "notes_label": "Notizen",
        "notes_placeholder": "Notizen eingeben...",
        "payback_label": "Amortisationszeit (Jahre)",
        "crossover_title": "Zusatzgewinn (vs Std)",
        "t_prod": "Produktion/Jahr",
        "t_oee": "Effizienz (OEE)",
        "t_scrap": "Ausschuss",
        "t_cons": "Energieverbrauch",
        "chart_years": "Jahre",
        "chart_profit": "Nettoüberschuss",
        "cost_kg": "Stückkosten (pro kg)",
        "margin_yr": "Operative Marge",
        "roi_ann": "ROI p.a.",
        "extra_5y": "5-Jahres-Zusatzprofit",
        "market_settings": "Markteinstellungen"
    },
    "Español": {
        "title": "ROI Extrusion Strategic Advisor",
        "tech_comp": "📊 Comparativa Técnica",
        "fin_comp": "💰 Rendimiento Financiero",
        "res_title": "🏁 Resultados ROI",
        "line_a": "Estándar",
        "line_b": "Premium",
        "line_c": "Fusion",
        "notes_label": "Notas",
        "notes_placeholder": "Escribir notas...",
        "payback_label": "Periodo de Retorno (Años)",
        "crossover_title": "Beneficio Extra (vs Std)",
        "t_prod": "Producción Anual",
        "t_oee": "Eficiencia (OEE)",
        "t_scrap": "Desperdicio",
        "t_cons": "Consumo Específico",
        "chart_years": "Años",
        "chart_profit": "Excedente Neto",
        "cost_kg": "Costo Unitario (por kg)",
        "margin_yr": "Margen Operativo",
        "roi_ann": "ROI Anualizado",
        "extra_5y": "Beneficio Extra 5 años",
        "market_settings": "Ajustes de Mercado"
    }
}

st.set_page_config(page_title="ROI Advisor", layout="wide")
lingua = st.sidebar.selectbox("Language", list(lang_dict.keys()), index=0)
t = lang_dict[lingua]
st.title(t['title'])

# --- SIDEBAR: MARKET SETTINGS ---
st.sidebar.header(f"🌍 {t['market_settings']}")
valuta_sel = st.sidebar.radio("Currency", ["EUR", "USD"])
simbolo = "€" if valuta_sel == "EUR" else "$"
cambio = st.sidebar.number_input("Exchange Rate (1€ = X $)", value=1.08) if valuta_sel == "USD" else 1.0

c_poly = st.sidebar.number_input(f"Polymer Cost ({simbolo}/kg)", value=1.50)
p_sell = st.sidebar.number_input(f"Selling Price ({simbolo}/kg)", value=2.10)
c_ene = st.sidebar.number_input(f"Energy Cost ({simbolo}/kWh)", value=0.22)
h_an = st.sidebar.number_input("Hours/Year", value=7500)
show_fusion = st.sidebar.checkbox("Show Fusion Line", value=False)

# --- INPUT COMPARISON ---
cols = st.columns(3 if show_fusion else 2)
with cols[0]:
    st.subheader(f"⚪ {t['line_a']}")
    ca = st.number_input("CAPEX Standard", value=1500000, key="ca")
    pa = st.number_input("Output (kg/h) Std", value=400, key="pa")
    oa = st.number_input("OEE (%) Std", value=83.0, key="oa")
    scra = st.number_input("Scrap (%) Std", value=2.5, key="scra")
    csa = st.number_input("kWh/kg Std", value=0.42, key="csa")

with cols[1]:
    st.subheader(f"💎 {t['line_b']}")
    cp = st.number_input("CAPEX Premium", value=2100000, key="cp")
    pp = st.number_input("Output (kg/h) Prem", value=450, key="pp")
    op = st.number_input("OEE (%) Prem", value=88.0, key="op")
    scrp = st.number_input("Scrap (%) Prem", value=1.5, key="scrp")
    csp = st.number_input("kWh/kg Prem", value=0.34, key="csp")

if show_fusion:
    with cols[2]:
        st.subheader(f"🌀 {t['line_c']}")
        cf = st.number_input("CAPEX Fusion", value=2400000, key="cf")
        pf = st.number_input("Output (kg/h) Fusion", value=450, key="pf")
        of = st.number_input("OEE (%) Fusion", value=91.0, key="of")
        scrf = st.number_input("Scrap (%) Fusion", value=1.0, key="scrf")
        csf = st.number_input("kWh/kg Fusion", value=0.28, key="csf")

# --- CALCULATIONS ---
def get_metrics(p, o, scr, cs, cap, cost_p):
    ton = (p * h_an * (o/100) * (1 - scr/100)) / 1000
    opex = (p * h_an * (o/100) * cost_p) + (p * h_an * (o/100) * cs * c_ene) + (cap * 0.02)
    marg = (ton * 1000 * p_sell) - opex
    ckg = opex / (ton * 1000)
    pb = cap / marg if marg > 0 else 0
    return ton, marg, ckg, pb

ton_a, marg_a, ckg_a, pb_a = get_metrics(pa, oa, scra, csa, ca, c_poly)
ton_b, marg_b, ckg_b, pb_b = get_metrics(pp, op, scrp, csp, cp, c_poly)
if show_fusion:
    ton_c, marg_c, ckg_c, pb_c = get_metrics(pf, of, scrf, csf, cf, c_poly * 0.95)

# --- TABLES ---
st.subheader(t['tech_comp'])
tech_data = {
    "Metric": [t['t_prod'], t['t_oee'], t['t_scrap'], t['t_cons']],
    "Standard": [f"{ton_a:,.0f} T", f"{oa}%", f"{scra}%", f"{csa}"],
    "Premium": [f"{ton_b:,.0f} T", f"{op}%", f"{scrp}%", f"{csp}"]
}
if show_fusion: tech_data["Fusion"] = [f"{ton_c:,.0f} T", f"{of}%", f"{scrf}%", f"{csf}"]
st.table(pd.DataFrame(tech_data))

st.subheader(t['fin_comp'])
fin_data = {
    "Indicator": [t['cost_kg'], t['margin_yr'], t['roi_ann'], t['payback_label'], t['extra_5y']],
    "Standard": [f"{ckg_a:.3f}", f"{marg_a:,.0f}", f"{(marg_a/ca)*100:.1f}%", f"{pb_a:.2f}", "-"],
    "Premium": [f"{ckg_b:.3f}", f"{marg_b:,.0f}", f"{(marg_b/cp)*100:.1f}%", f"{pb_b:.2f}", f"{(marg_b-marg_a)*5:,.0f}"]
}
if show_fusion:
    fin_data["Fusion"] = [f"{ckg_c:.3f}", f"{marg_c:,.0f}", f"{(marg_c/cf)*100:.1f}%", f"{pb_c:.2f}", f"{(marg_c-marg_a)*5:,.0f}"]
st.table(pd.DataFrame(fin_data))

# --- CHARTS ---
st.header(t['res_title'])
c1, c2 = st.columns(2)
with c1:
    names = [t['line_a'], t['line_b']]
    vals = [pb_a, pb_b]
    if show_fusion:
        names.append(t['line_c'])
        vals.append(pb_c)
    fig_pb = go.Figure(go.Bar(y=names, x=vals, orientation='h', marker_color='#00CC96'))
    fig_pb.update_layout(title=t['payback_label'], xaxis_title=t['chart_years'], yaxis={'autorange': "reversed"})
    st.plotly_chart(fig_pb, use_container_width=True)

with c2:
    yrs = [i/2 for i in range(13)]
    fig_cross = go.Figure()
    fig_cross.add_trace(go.Scatter(x=yrs, y=[(-(cp-ca)+(marg_b-marg_a)*y) for y in yrs], name=t['line_b']))
    if show_fusion:
        fig_cross.add_trace(go.Scatter(x=yrs, y=[(-(cf-ca)+(marg_c-marg_a)*y) for y in yrs], name=t['line_c']))
    fig_cross.add_hline(y=0, line_dash="dash", line_color="red")
    fig_cross.update_layout(title=t['crossover_title'], xaxis_title=t['chart_years'])
    st.plotly_chart(fig_cross, use_container_width=True)

st.divider()
notes = st.text_area(t['notes_label'], placeholder=t['notes_placeholder'], height=100)
