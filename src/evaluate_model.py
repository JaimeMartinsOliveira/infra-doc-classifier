import pandas as pd
import pickle
from sklearn.metrics import classification_report, accuracy_score

def avaliar_modelo(caminho_dados: str, caminho_modelo: str, caminho_vectorizer: str):
    print("Carregando dados de validação...")
    df = pd.read_csv(caminho_dados)

    if 'text_limpo' not in df.columns or 'label' not in df.columns:
        raise ValueError("O CSV precisa conter as colunas 'text_limpo' e 'label'.")

    X_val = df['text_limpo']
    y_val = df['label']

    print("Carregando modelo e vetor TF-IDF...")
    with open(caminho_modelo, 'rb') as f:
        modelo = pickle.load(f)
    with open(caminho_vectorizer, 'rb') as f:
        vectorizer = pickle.load(f)

    print("Transformando textos...")
    X_val_vec = vectorizer.transform(X_val)

    print("Fazendo previsões...")
    y_pred = modelo.predict(X_val_vec)

    print("\n📊 Relatório de Classificação:")
    print(classification_report(y_val, y_pred))

    print(f"✅ Acurácia: {accuracy_score(y_val, y_pred):.2f}")


if __name__ == "__main__":
    CAMINHO_DADOS = "data/exemplo_tratado.csv"
    CAMINHO_MODELO = "models/modelo_classificador.pkl"
    CAMINHO_VECTORIZER = "models/tfidf_vectorizer.pkl"

    avaliar_modelo(CAMINHO_DADOS, CAMINHO_MODELO, CAMINHO_VECTORIZER)
