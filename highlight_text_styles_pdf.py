import streamlit as st
import fitz  # PyMuPDF
import tempfile

st.set_page_config(page_title="Destacar Negrito e Itálico em PDFs", page_icon="🟡")

st.title("🟡 Destacar Negrito e Itálico em PDFs")
st.write("Envie seus arquivos PDF e o aplicativo gerará versões com os trechos em negrito (amarelo) e itálico (azul).")

uploaded_files = st.file_uploader("📂 Envie um ou mais PDFs", type="pdf", accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        st.write(f"📄 Processando: **{file.name}**")

        # Lê PDF temporariamente
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_input:
            temp_input.write(file.read())
            temp_input.flush()

            doc = fitz.open(temp_input.name)

            bold_fonts, italic_fonts = set(), set()

            # Identifica fontes
            for page in doc:
                for block in page.get_text("dict")["blocks"]:
                    if "lines" not in block:
                        continue
                    for line in block["lines"]:
                        for span in line["spans"]:
                            font_name = span["font"].lower()
                            if "bold" in font_name or "medium" in font_name:
                                bold_fonts.add(font_name)
                            if "italic" in font_name or "oblique" in font_name:
                                italic_fonts.add(font_name)

            # Destaca textos
            for page in doc:
                for block in page.get_text("dict")["blocks"]:
                    if "lines" not in block:
                        continue
                    for line in block["lines"]:
                        for span in line["spans"]:
                            font_name = span["font"].lower()
                            bbox = span["bbox"]  # [x0, y0, x1, y1]
                            rect = fitz.Rect(bbox)

                            # Decide a cor do destaque
                            color = None
                            if any(k in font_name for k in bold_fonts):
                                color = (1, 1, 0)   # amarelo (RGB 0-1)
                            if any(k in font_name for k in italic_fonts):
                                # se um span for itálico (ou itálico+negrito), dá prioridade ao azul
                                color = (0, 0.6, 1) # azul

                            if color:
                                annot = page.add_rect_annot(rect)
                                annot.set_colors(stroke=None, fill=color)
                                annot.set_opacity(0.35)  # transparência estilo marca-texto
                                annot.update()

            # 3️⃣ Salva e oferece download
            with tempfile.NamedTemporaryFile(delete=False, suffix="_destacado.pdf") as temp_out:
                doc.save(temp_out.name)
                doc.close()
                st.success(f"✅ Finalizado: **{file.name}**")
                with open(temp_out.name, "rb") as f:
                    st.download_button(
                        label="⬇️ Baixar PDF destacado",
                        data=f.read(),
                        file_name=file.name.replace(".pdf", "_destacado.pdf"),
                        mime="application/pdf",
                    )
