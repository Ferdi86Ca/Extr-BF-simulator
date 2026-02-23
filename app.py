import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# --- DIZIONARIO TRADUZIONI ---
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
    "Deutsch": { "title": "ROI Extrusion Strategic Advisor", "tech_comp": "📊 Technischer Vergleich", "fin_comp": "💰 Finanzielle Performance", "res_title": "🏁 ROI-Ergebnisse", "line_a": "Standard", "line_b": "Premium", "line_c": "Fusion", "notes_label": "Notizen", "notes_placeholder": "Notizen...", "payback_label": "Amortisationszeit (Jahre)", "crossover_title": "Zusatzgewinn", "t_prod": "Produktion/Jahr", "t_oee": "Effizienz (OEE)", "t_scrap": "Ausschuss", "t_cons": "Energieverbrauch", "chart_years": "Jahre", "chart_profit": "Nettoüberschuss", "cost_kg": "Stückkosten", "margin_yr": "Marge", "roi_ann": "ROI", "extra_5y": "5-J-Zusatzprofit", "market_settings": "Einstellungen" },
    "Español": { "title": "ROI Extrusion Strategic Advisor", "tech_comp": "📊 Comparativa Técnica", "fin_comp": "💰 Rendimiento Financiero", "res_title": "🏁 Resultados ROI", "line_a": "Estándar", "line_b": "Premium", "line_c": "Fusion", "notes_label": "Notas", "notes_placeholder": "Notas...", "payback_label": "Payback (Años)", "crossover_title": "Beneficio Extra", "t_prod": "Producción Anual", "t_oee": "Eficiencia", "t_scrap": "Desperdicio", "t_cons": "Consumo", "chart_years": "Años", "chart_profit": "Excedente", "cost_kg": "Costo/kg", "margin_yr": "Margen Anual", "roi_ann": "ROI", "extra_5y": "Extra 5 años", "market_settings": "Ajustes" }
}

st.set_page_config(page_title="ROI Advisor", layout="wide")
lingua = st.sidebar.selectbox("Language", list(lang_dict.keys()), index=0)
t = lang_dict[lingua]

# --- COLORS ---
color_a = "#636EFA" # Blue
color_b = "#00CC96" # Green
color_c = "#AB63FA" # Purple

# --- SIDEBAR: MARKET SETTINGS ---
st.sidebar.header(f"🌍 {t['market_settings']}")
valuta_sel = st.sidebar.radio("Currency", ["EUR", "USD"])
simbolo = "€" if valuta_sel == "EUR" else "$"
cambio = st.sidebar.number_input("Exchange Rate (1€ = X $)", value=1.08) if valuta_sel == "USD" else 1.0

c_poly = st.sidebar.number_input(f"Polymer Cost ({simbolo}/kg)", value=1.50)
p_sell = st.sidebar.number_input(f"Selling Price ({simbolo}/kg)", value=2.00)
c_ene = st.sidebar.number_input(f"Energy Cost ({simbolo}/kWh)", value=0.22)
h_an = st.sidebar.number_input("Hours/Year", value=7500)
tol_m = st.sidebar.slider("Market Tol. (±%)", 1.0, 10.0, 6.0)
show_fusion = st.sidebar.checkbox("Show Fusion Line", value=False)

# --- INPUT COMPARISON (RIPRISTINATI PARAMETRI ORIGINALI) ---
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
        of = 87.0 # Pareggiato a Premium come da logica precedente
        sf = st.number_input("2-Sigma (%) Fusion", value=1.5)
        scrf = st.number_input("Scrap (%) Fusion", value=1.5)
        mf_fus = st.number_input("Maint. % Fusion", value=1.5)
        csf = st.number_input("kWh/kg Fusion", value=0.28)
        c_poly_f = st.number_input(f"Polymer Cost Fusion ({simbolo}/kg)", value=1.35)
else:
    c_poly_f = c_poly

# --- CALCULATIONS ---
def get_metrics(p, o, s, scr, cs, m, cap, cost_p):
    ton = (p * h_an * (o/100) * (1 - scr/100)) / 1000
    mat_eff = 1 - (tol_m - s)/100
    opex = (p * h_an * (o/100) * cost_p * mat_eff) + (p * h_an * (o/100) * cs * c_ene) + (cap * m/100)
    marg = (ton * 1000 * p_sell) - opex
    ckg = opex / (ton * 1000) if ton > 0 else 0
    pb = cap / marg if marg > 0 else 0
    return ton, marg, ckg, pb

ton_a, marg_a, ckg_a, pb_a = get_metrics(pa, oa, sa, scra, csa, ma_std, ca, c_poly)
ton_b, marg_b, ckg_b, pb_b = get_metrics(pp, op, sp, scrp, csp, mp_pre, cp, c_poly)
if show_fusion:
    ton_c, marg_c, ckg_c, pb_c = get_metrics(pf, of, sf, scrf, csf, mf_fus, cf, c_poly_f)

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

# --- CHARTS CON COLORI MIGLIORATI ---
st.header(t['res_title'])
c1, c2 = st.columns(2)
with c1:
    names = [t['line_a'], t['line_b']]
    vals = [pb_a, pb_b]
    colors = [color_a, color_b]
    if show_fusion:
        names.append(t['line_c'])
        vals.append(pb_c)
        colors.append(color_c)
    
    fig_pb = go.Figure(go.Bar(y=names, x=vals, orientation='h', marker_color=colors))
    fig_pb.update_layout(title=t['payback_label'], xaxis_title=t['chart_years'], yaxis={'autorange': "reversed"})
    st.plotly_chart(fig_pb, use_container_width=True)

with c2:
    yrs = [i/2 for i in range(13)]
    fig_cross = go.Figure()
    fig_cross.add_trace(go.Scatter(x=yrs, y=[(-(cp-ca)+(marg_b-marg_a)*y) for y in yrs], name=t['line_b'], line=dict(color=color_b, width=4)))
    if show_fusion:
        fig_cross.add_trace(go.Scatter(x=yrs, y=[(-(cf-ca)+(marg_c-marg_a)*y) for y in yrs], name=t['line_c'], line=dict(color=color_c, width=4)))
    fig_cross.add_hline(y=0, line_dash="dash", line_color="red")
    fig_cross.update_layout(title=t['crossover_title'], xaxis_title=t['chart_years'], hovermode="x unified")
    st.plotly_chart(fig_cross, use_container_width=True)

st.divider()
notes = st.text_area(t['notes_label'], placeholder=t['notes_placeholder'], height=100)
