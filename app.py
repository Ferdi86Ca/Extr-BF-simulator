def create_pdf(data_dict, lang_t, simbolo, val_code, line_a_data, line_p_data):
    pdf = FPDF()
    pdf.add_page()
    
    # Intestazione
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt=lang_t['title'], ln=True, align='C')
    pdf.set_font("Arial", "I", 10)
    pdf.cell(200, 10, txt="Confidential Strategic Comparison", ln=True, align='C')
    pdf.ln(10)
    
    # 1. ANALISI ECONOMICA (KPI)
    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(190, 10, txt=" 1. " + lang_t['res_title'].upper(), ln=True, fill=True)
    pdf.ln(2)
    
    pdf.set_font("Arial", "", 10)
    metrics = [
        (lang_t['extra_margin'], f"{simbolo} {data_dict['dmarg']:,.0f}"),
        (lang_t['extra_tons'], f"{data_dict['diff_tons']:,.0f} T/y"),
        (lang_t['payback'], f"{data_dict['pbk']:.1f} Years"),
        (lang_t['profit_5y'], f"{simbolo} {data_dict['p5y']:,.0f}"),
        (lang_t['cost_kg'] + " (Saving)", f"{simbolo} {data_dict['saving']:.3f}")
    ]
    
    for m in metrics:
        pdf.cell(95, 8, m[0], 1)
        pdf.cell(95, 8, m[1], 1, 1, 'C')
    
    pdf.ln(10)

    # 2. TABELLA COMPARATIVA TECNICA
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, txt=" 2. " + lang_t['tech_comp'].upper(), ln=True, fill=True)
    pdf.ln(2)
    
    pdf.set_font("Arial", "B", 9)
    # Header Tabella
    pdf.cell(60, 10, "Parameter", 1, 0, 'C')
    pdf.cell(65, 10, lang_t['line_a'], 1, 0, 'C')
    pdf.cell(65, 10, lang_t['line_b'], 1, 1, 'C')
    
    pdf.set_font("Arial", "", 9)
    # Righe della tabella
    tech_rows = [
        (lang_t['annual_prod'], f"{line_a_data['tons']:,.0f} T", f"{line_p_data['tons']:,.0f} T"),
        (lang_t['output'], f"{line_a_data['out']} kg/h", f"{line_p_data['out']} kg/h"),
        (lang_t['oee'], f"{line_a_data['oee']}%", f"{line_p_data['oee']}%"),
        (lang_t['scrap'], f"{line_a_data['scr']}%", f"{line_p_data['scr']}%"),
        (lang_t['precision'], f"{line_a_data['pre']} %", f"{line_p_data['pre']} %")
    ]
    
    for r in tech_rows:
        pdf.cell(60, 8, r[0], 1)
        pdf.cell(65, 8, r[1], 1, 0, 'C')
        pdf.cell(65, 8, r[2], 1, 1, 'C')

    pdf.ln(10)

    # 3. EXECUTIVE SUMMARY
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, txt=" 3. EXECUTIVE SUMMARY", ln=True, fill=True)
    pdf.ln(2)
    pdf.set_font("Arial", "", 10)
    
    summary = (f"The Premium Line represents the most efficient industrial choice. Through superior 2-sigma precision "
               f"and optimized OEE ({line_p_data['oee']}%), the plant will deliver an additional {data_dict['diff_tons']:,.0f} "
               f"tons of sellable film annually. The significant reduction in production cost per KG ensures that "
               f"the initial investment gap is recovered in just {data_dict['pbk']:.1f} years.")
    
    pdf.multi_cell(190, 7, txt=summary)
    
    return pdf.output(dest='S').encode('latin-1')
