import streamlit as st
import plotly.graph_objects as go

# Configurazione Pagina
st.set_page_config(page_title="ROI Estrusione Pro", layout="centered")

st.title("📊 Simulatore ROI Film in Bolla")
st.write("Confronto tecnico-economico avanzato")

# --- SIDEBAR: PARAMETRI GENERALI ---
st.sidebar.header("Parametri Generali")
costo_pe = st.sidebar.number_input("Costo Polimero (€/kg)", value=1.50)
prezzo_vendita = st.sidebar.number_input("Prezzo Vendita Film (€/kg)", value=2.80)
costo_en = st.sidebar.number_input("Costo Energia (€/kWh)", value=0.25)
ore_anno = st.sidebar.number_input("Ore produzione/anno", value=7500)
tolleranza_mercato = st.sidebar.slider("Tolleranza Media Mercato (±%)", 1.0, 10.0, 6.0)

# --- CORPO CENTRALE: CONFRONTO MACCHINE ---
st.header("Confronto Linee di Estrusione")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Linea A (Standard)")
    capex_a = st.number_input("Investimento A (€)", value=650000)
    portata_a = st.number_input("Portata Oraria A (kg/h)", value=400)
    cons_a = st.number_input("Consumo A (kWh/kg)", value=0.60)
    sigma_a = st.number_input("Precisione 2σ A (±%)", value=5.5)

with col2:
    st.subheader("Linea B (Premium)")
    capex_b = st.number_input("Investimento B (€)", value=900000)
    portata_b = st.number_input("Portata Oraria B (kg/h)", value=440)
    cons_b = st.number_input("Consumo B (kWh/kg)", value=0.42)
    sigma_b = st.number_input("Precisione 2σ B (±%)", value=1.5)

# --- LOGICA DI CALCOLO ---
prod_annua_a = portata_a * ore_anno
prod_annua_b = portata_b * ore_anno

# 1. Risparmio Materia Prima (Down-gauging)
risparmio_mat_percentuale = (tolleranza_mercato - sigma_b) / 100
risparmio_mat_annuo = prod_annua_b * costo_pe * risparmio_mat_percentuale

# 2. Extra Ricavo (Maggiore portata)
extra_ricavo_produzione = (prod_annua_b - prod_annua_a) * (prezzo_vendita - costo_pe)

# 3. Risparmio Energetico
costo_en_a = prod_annua_a * cons_a * costo_en
costo_en_b = prod_annua_b * cons_b * costo_en
risparmio_energia_annuo = costo_en_a - costo_en_b

# 4. Margine Operativo Extra e Payback
margine_extra_totale = risparmio_mat_annuo + risparmio_energia_annuo + extra_ricavo_produzione
delta_investimento = capex_b - capex_a
payback = delta_investimento / margine_extra_totale if margine_extra_totale > 0 else 0

# --- OUTPUT RISULTATI ---
st.divider()
st.subheader("🏁 Analisi del Ritorno (ROI)")
c1, c2 = st.columns(2)
c1.metric("Margine Extra Annuo", f"€ {margine_extra_totale:,.0f}")
c2.metric("Punto di Pareggio", f"{payback:.1f} Anni")

# --- GRAFICO 1: RISPARMIO ACCUMULATO ---
anni = [0, 1, 2, 3, 4, 5]
risparmi_y = [margine_extra_totale * i for i in anni]
fig1 = go.Figure()
fig1.add_trace(go.Bar(x=anni[1:], y=risparmi_y[1:], name="Risparmio Extra", marker_color='#2ca02c'))
fig1.add_hline(y=delta_investimento, line_dash="dash", line_color="red", annotation_text="Extra Costo Macchina B")
st.plotly_chart(fig1, use_container_width=True)

# --- GRAFICO 2: BREAK-EVEN (CORRETTO) ---
st.subheader("📈 Cash-Flow: Linea A vs Linea B")
margine_base_a = (prod_annua_a * (prezzo_vendita - costo_pe)) - costo_en_a
margine_base_b = (prod_annua_b * (prezzo_vendita - costo_pe)) - costo_en_b + risparmio_mat_annuo

flusso_a = [-capex_a + (margine_base_a * i) for i in anni]
flusso_b = [-capex_b + (margine_base_b * i) for i in anni]

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=anni, y=flusso_a, name="Linea Standard A", line=dict(color='gray', dash='dot')))
fig2.add_trace(go.Scatter(x=anni, y=flusso_b, name="Linea Premium B", line=dict(color='#00CC96', width=4)))
fig2.add_hline(y=0, line_color="black")
fig2.update_layout(xaxis_title="Anni", yaxis_title="Profitto Cumulativo (€)")
st.plotly_chart(fig2, use_container_width=True)

# --- TASTO SCARICA REPORT ---
st.divider()
report_text = f"""REPORT SIMULAZIONE ROI
---------------------------
DATI DI MERCATO:
Costo Polimero: {costo_pe} €/kg
Costo Energia: {costo_en} €/kWh
Ore/Anno: {ore_anno}

RISULTATI CONFRONTO:
Extra Investimento: € {delta_investimento:,.2f}
Risparmio Annuo Totale: € {margine_extra_totale:,.2f}
Payback Period: {payback:.1f} anni

VANTAGGI TECNICI LINEA B:
- Risparmio polimero (Down-gauging): € {risparmio_mat_annuo:,.2f}
- Risparmio energetico: € {risparmio_energia_annuo:,.2f}
"""

st.download_button(
    label="📩 Scarica Report per il Cliente",
    data=report_text,
    file_name="report_roi_estrusione.txt",
    mime="text/plain"
)
