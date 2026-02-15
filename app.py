import streamlit as st

# Configurazione pagina per Mobile
st.set_page_config(page_title="Estrusione ROI", layout="centered")

st.title("🚀 Simulatore ROI Estrusione")
st.write("Confronto immediato tra due tecnologie")

# --- INPUT DI MERCATO (In alto, espandibile) ---
with st.expander("Parametri di Mercato (Costi attuali)"):
    costo_pe = st.number_input("Costo Polimero (€/kg)", value=1.50, step=0.1)
    costo_en = st.slider("Costo Energia (€/kWh)", 0.10, 0.60, 0.25)
    ore_anno = st.number_input("Ore produzione/anno", value=7000)

# --- CONFRONTO LINEE ---
st.header("Confronto Linee")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Standard")
    capex_a = st.number_input("Prezzo A (€)", value=600000)
    cons_a = st.number_input("Consumo A (kWh/kg)", value=0.60)
    prec_a = st.number_input("Precisione A (±%)", value=5.0)

with col2:
    st.subheader("Premium")
    capex_b = st.number_input("Prezzo B (€)", value=850000)
    cons_b = st.number_input("Consumo B (kWh/kg)", value=0.42)
    prec_b = st.number_input("Precisione B (±%)", value=1.5)

# --- LOGICA CALCOLO RAPIDO ---
output_medio = 400 # kg/h
risparmio_energia = (cons_a - cons_b) * output_medio * ore_anno * costo_en
# Efficienza spessore (Down-gauging)
risparmio_materiale = ((prec_a - prec_b)/100) * output_medio * ore_anno * costo_pe

risparmio_totale = risparmio_energia + risparmio_materiale
delta_investimento = capex_b - capex_a
payback = delta_investimento / risparmio_totale if risparmio_totale > 0 else 0

# --- RISULTATI IMPATTANTI ---
st.divider()
st.subheader("Risultato della Simulazione")
st.metric("Risparmio Annuo Totale", f"€ {risparmio_totale:,.0f}")

if payback > 0:
    st.success(f"L'investimento Premium si ripaga in soli {payback:.1f} anni")
else:
    st.error("Verificare i parametri di input")

# Bottone per resettare o inviare log
if st.button("Invia Simulazione via Email"):
    st.write("Funzione configurabile per inviare il PDF al cliente.")

# --- CALCOLO E GRAFICO IMPATTO 5 ANNI ---
st.divider()
st.subheader("💰 Impatto Economico nel Tempo")

# Creiamo i dati per i prossimi 5 anni
anni = [1, 2, 3, 4, 5]
risparmio_annuo_fisso = risparmio_totale # Il dato calcolato prima
risparmio_cumulativo = [risparmio_annuo_fisso * i for i in anni]

# Creiamo il grafico
import plotly.graph_objects as go

fig = go.Figure()

# Bar chart per il risparmio
fig.add_trace(go.Bar(
    x=anni, 
    y=risparmio_cumulativo,
    name="Guadagno Extra Accumulato",
    marker_color='#2ca02c'
))

# Linea orizzontale che rappresenta il costo extra della macchina B
fig.add_hline(
    y=delta_investimento, 
    line_dash="dash", 
    line_color="red", 
    annotation_text="Costo Extra Macchina Premium",
    annotation_position="top left"
)

fig.update_layout(
    title="Ritorno dell'investimento extra (5 anni)",
    xaxis_title="Anni di produzione",
    yaxis_title="Euro (€)",
    template="plotly_white",
    hovermode="x unified"
)

# Mostra il grafico nell'app
st.plotly_chart(fig, use_container_width=True)
