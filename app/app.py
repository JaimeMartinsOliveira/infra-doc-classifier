import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import fitz  # PyMuPDF
from src.inference import classificar_texto


def extrair_texto_pdf(file):
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        texto = ""
        for page in doc:
            texto += page.get_text()
    return texto


def extrair_texto_txt(file):
    return file.read().decode("utf-8")


# Configuração da página
st.set_page_config(page_title="Classificador de Documentos Técnicos", layout="centered")
st.title("📁 Classificador de Documentos Técnicos de Infraestrutura")
st.markdown(
    """
    Este assistente classifica documentos técnicos em categorias como **Mineração**, **Energia**, **Rodovias**, **Saneamento**, etc.

    🧠 Digite o texto ou envie um arquivo PDF/TXT para análise.
    """
)

# Escolha do modo de entrada
modo = st.radio("📥 Escolha como deseja inserir o documento:", ("Digitar texto", "Upload de arquivo"))

texto_input = ""

if modo == "Digitar texto":
    texto_input = st.text_area("✍️ Digite ou cole o conteúdo do documento:", height=200)

elif modo == "Upload de arquivo":
    uploaded_file = st.file_uploader("📎 Envie um arquivo .pdf ou .txt", type=["pdf", "txt"])
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".pdf"):
            texto_input = extrair_texto_pdf(uploaded_file)
        elif uploaded_file.name.endswith(".txt"):
            texto_input = extrair_texto_txt(uploaded_file)

        st.text_area("📄 Conteúdo extraído do arquivo:", value=texto_input, height=200)

# Botão de classificação
if st.button("🔍 Classificar"):
    if texto_input.strip() == "":
        st.warning("Por favor, forneça algum conteúdo para classificar.")
    else:
        categoria, confianca = classificar_texto(texto_input)
        st.success(f"📂 Categoria prevista: **{categoria}**")
        st.info(f"🔍 Nível de confiança: **{confianca:.2%}**")
