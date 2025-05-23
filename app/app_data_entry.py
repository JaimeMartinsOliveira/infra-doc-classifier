import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
import os

st.set_page_config(page_title="Upload e Extração de Documentos 📄")

def extrair_blocos_pdf(file) -> list:
    doc = fitz.open(stream=file.read(), filetype="pdf")
    blocos = []
    for pagina in doc:
        texto = pagina.get_text("blocks")  # lista de blocos da página
        for bloco in texto:
            blocos.append(bloco[4].strip())
    return [b for b in blocos if b]

def extrair_blocos_txt(file) -> list:
    content = file.read().decode('utf-8')
    linhas = content.splitlines()
    blocos = [linha.strip() for linha in linhas if linha.strip()]
    return blocos

def salvar_blocos_csv(blocos, nome_arquivo='blocos_extraidos.csv'):
    pasta_saida = 'data/processed'
    os.makedirs(pasta_saida, exist_ok=True)
    df = pd.DataFrame({
        'bloco_numero': list(range(1, len(blocos)+1)),
        'texto': blocos
    })
    caminho_arquivo = os.path.join(pasta_saida, nome_arquivo)
    df.to_csv(caminho_arquivo, index=False, encoding='utf-8-sig')
    return caminho_arquivo

st.title("Upload e Extração de Documentos 📄")

uploaded_file = st.file_uploader(
    "Faça upload do arquivo PDF ou TXT",
    type=["pdf", "txt"],
    help="Limite de 200 MB por arquivo"
)

# Inicializa sessão blocos para exportação
if 'blocos' not in st.session_state:
    st.session_state.blocos = []

# Botão exportar sempre visível
if st.button("📤 Exportar CSV"):
    if st.session_state.blocos:
        caminho_csv = salvar_blocos_csv(st.session_state.blocos)
        st.success(f"Arquivo CSV salvo em: {caminho_csv}")
        st.markdown(f"[Clique aqui para baixar o CSV]({caminho_csv})")
    else:
        st.warning("Nenhum bloco para exportar.")

if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        blocos = extrair_blocos_pdf(uploaded_file)
    elif uploaded_file.type == "text/plain":
        blocos = extrair_blocos_txt(uploaded_file)
    else:
        st.error("Formato de arquivo não suportado.")
        blocos = []

    if blocos:
        st.write(f"Número de blocos detectados: {len(blocos)}")
        for i, bloco in enumerate(blocos, 1):
            st.markdown(f"📦 **Bloco {i}**")
            st.write(bloco)
            st.markdown("---")
        st.session_state.blocos = blocos
    else:
        st.warning("Nenhum bloco detectado no arquivo.")
else:
    st.info("Faça o upload de um arquivo PDF ou TXT para começar.")
