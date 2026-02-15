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
