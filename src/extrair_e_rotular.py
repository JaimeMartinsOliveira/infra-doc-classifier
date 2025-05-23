import fitz  # PyMuPDF
import pandas as pd

def extrair_texto_pdf(caminho_pdf):
    doc = fitz.open(caminho_pdf)
    textos = []
    for pagina in doc:
        texto = pagina.get_text("text")
        textos.append(texto)
    return textos

def dividir_em_blocos(textos, separador="\n\n"):
    blocos = []
    for texto in textos:
        partes = texto.split(separador)
        blocos.extend([parte.strip() for parte in partes if parte.strip()])
    return blocos

def rotular_blocos(blocos):
    dados = []
    print("Instruções: Para cada bloco de texto, digite a categoria e pressione Enter.")
    print("Digite 'pular' para ignorar o bloco, ou 'sair' para terminar o processo.\n")

    for i, bloco in enumerate(blocos):
        print(f"\nBloco {i+1}:\n{bloco}\n")
        label = input("Categoria (ou pular/sair): ").strip()
        if label.lower() == "sair":
            break
        if label.lower() == "pular" or label == "":
            continue
        dados.append({"text": bloco, "label": label})
    return dados

def salvar_csv(dados, caminho_csv):
    df = pd.DataFrame(dados)
    df.to_csv(caminho_csv, index=False)
    print(f"\nCSV salvo em: {caminho_csv}")

if __name__ == "__main__":
    caminho_pdf = input("Digite o caminho do arquivo PDF: ")
    textos = extrair_texto_pdf(caminho_pdf)
    blocos = dividir_em_blocos(textos)
    dados_rotulados = rotular_blocos(blocos)
    caminho_csv = input("Digite o nome do arquivo CSV para salvar (ex: dados.csv): ")
    salvar_csv(dados_rotulados, caminho_csv)