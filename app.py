import streamlit as st
import plotly.graph_objects as go

# Configurazione Pagina
st.set_page_config(page_title="ROI Estrusione Pro", layout="centered")

st.title("📊 Simulatore ROI Film in Bolla")
st.write("Analisi basata su precisione $2\sigma$ e down-gauging.")

# --- SIDEBAR: PARAMETRI GENERALI (MERCATO) ---
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

# 1. Calcolo Risparmio Materia Prima (Effetto Down-gauging)
# Più la macchina è precisa (2sigma basso), più posso ridurre il set-point dello spessore
risparmio_mat_percentuale = (tolleranza_mercato - sigma_b) / 100
risparmio_mat_annuo = (portata_b * ore_anno) * costo_pe * risparmio_mat_percentuale

# 2. Calcolo Differenza Produzione Vendibile
prod_annua_a = portata_a * ore_anno
prod_annua_b = portata_b * ore_anno
extra_ricavo_produzione = (prod_annua_b - prod_annua_a) * (prezzo_vendita - costo_pe)

# 3. Calcolo Risparmio Energetico
costo_en_a = prod_annua_a * cons_a * costo_en
costo_en_b = prod_annua_b * cons_b * costo_en
risparmio_energia_annuo = costo_en_a - costo_en_b

# 4. Margine Operativo Extra Totale (B vs A)
margine_extra_totale = risparmio_mat_annuo + risparmio_energia_annuo + extra_ricavo_produzione
delta_investimento = capex_b - capex_a
payback = delta_investimento / margine_extra_totale if margine_extra_totale > 0 else 0

# --- VISUALIZZAZIONE RISULTATI ---
st.divider()
st.metric("Margine Extra Annuo (Linea B)", f"€ {margine_extra_totale:,.0f}")

if payback > 0:
    st.success(f"L'investimento extra si ripaga in {payback:.1f} anni")

# GRAFICO CUMULATIVO
anni = [1, 2, 3, 4, 5]
valori_cumulati = [margine_extra_totale * i for i in anni]

fig = go.Figure()
fig.add_trace(go.Bar(x=anni, y=valori_cumulati, name="Guadagno Extra Accumulato", marker_color='#2ca02c'))
fig.add_hline(y=delta_investimento, line_dash="dash", line_color="red", annotation_text="Costo Extra Macchina B")

fig.update_layout(title="Ritorno Economico in 5 Anni", xaxis_title="Anni", yaxis_title="Euro (€)")
st.plotly_chart(fig, use_container_width=True)

import streamlit as st
import plotly.graph_objects as go

# Configurazione Pagina
st.set_page_config(page_title="ROI Estrusione Pro", layout="centered")

st.title("📊 Simulatore ROI Film in Bolla")
st.write("Analisi basata su precisione $2\sigma$ e down-gauging.")

# --- SIDEBAR: PARAMETRI GENERALI (MERCATO) ---
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

# 1. Calcolo Risparmio Materia Prima (Effetto Down-gauging)
# Più la macchina è precisa (2sigma basso), più posso ridurre il set-point dello spessore
risparmio_mat_percentuale = (tolleranza_mercato - sigma_b) / 100
risparmio_mat_annuo = (portata_b * ore_anno) * costo_pe * risparmio_mat_percentuale

# 2. Calcolo Differenza Produzione Vendibile
prod_annua_a = portata_a * ore_anno
prod_annua_b = portata_b * ore_anno
extra_ricavo_produzione = (prod_annua_b - prod_annua_a) * (prezzo_vendita - costo_pe)

# 3. Calcolo Risparmio Energetico
costo_en_a = prod_annua_a * cons_a * costo_en
costo_en_b = prod_annua_b * cons_b * costo_en
risparmio_energia_annuo = costo_en_a - costo_en_b

# 4. Margine Operativo Extra Totale (B vs A)
margine_extra_totale = risparmio_mat_annuo + risparmio_energia_annuo + extra_ricavo_produzione
delta_investimento = capex_b - capex_a
payback = delta_investimento / margine_extra_totale if margine_extra_totale > 0 else 0

# --- VISUALIZZAZIONE RISULTATI ---
st.divider()
st.metric("Margine Extra Annuo (Linea B)", f"€ {margine_extra_totale:,.0f}")

if payback > 0:
    st.success(f"L'investimento extra si ripaga in {payback:.1f} anni")

# GRAFICO CUMULATIVO
anni = [1, 2, 3, 4, 5]
valori_cumulati = [margine_extra_totale * i for i in anni]

fig = go.Figure()
fig.add_trace(go.Bar(x=anni, y=valori_cumulati, name="Guadagno Extra Accumulato", marker_color='#2ca02c'))
fig.add_hline(y=delta_investimento, line_dash="dash", line_color="red", annotation_text="Costo Extra Macchina B")

fig.update_layout(title="Ritorno Economico in 5 Anni", xaxis_title="Anni", yaxis_title="Euro (€)")
st.plotly_chart(fig, use_container_width=True)
