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

            # 1️⃣ Identifica fontes
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

            # 2️⃣ Destaca textos
            for page in doc:
                for block in page.get_text("dict")["blocks"]:
                    if "lines" not in block:
                        continue
                    for line in block["lines"]:
                        for span in line["spans"]:
                            font_name = span["font"].lower()
                            bbox = span["bbox"]
