import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')


def limpar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r'[^\w\s]', '', texto)  # Remove pontuação
    tokens = word_tokenize(texto, language='portuguese')
    stop_words = set(stopwords.words('portuguese'))
    tokens_filtrados = [t for t in tokens if t not in stop_words]
    return ' '.join(tokens_filtrados)


def preprocessar_csv(caminho_csv: str, caminho_saida: str):
    df = pd.read_csv(caminho_csv)

    if 'texto' not in df.columns:
        raise ValueError("O CSV precisa conter a coluna 'texto'.")

    print("Iniciando pré-processamento...")

    df['text_limpo'] = df['texto'].astype(str).apply(limpar_texto)

    # Se não existir a coluna label, cria com valor padrão 'Outros'
    if 'label' not in df.columns:
        df['label'] = 'Outros'

    df.to_csv(caminho_saida, index=False)
    print(f"Pré-processamento concluído. Arquivo salvo em: {caminho_saida}")


if __name__ == "__main__":
    entrada = "data/exemplo.csv"
    saida = "data/exemplo_tratado.csv"
    preprocessar_csv(entrada, saida)
