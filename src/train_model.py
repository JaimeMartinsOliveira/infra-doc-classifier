import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

def treinar_modelo(caminho_dados: str, caminho_modelo: str, caminho_vectorizer: str):
    print("Carregando dados...")
    df = pd.read_csv(caminho_dados)

    if 'text_limpo' not in df.columns or 'label' not in df.columns:
        raise ValueError("O CSV precisa conter as colunas 'text_limpo' e 'label'.")

    X = df['text_limpo']
    y = df['label']

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Vetorizando textos...")
    vectorizer = TfidfVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_val_vec = vectorizer.transform(X_val)

    print("Treinando modelo...")
    modelo = LogisticRegression(max_iter=1000)
    modelo.fit(X_train_vec, y_train)

    print("Avaliando modelo...")
    y_pred = modelo.predict(X_val_vec)
    print(classification_report(y_val, y_pred))

    with open(caminho_modelo, 'wb') as f:
        pickle.dump(modelo, f)
    with open(caminho_vectorizer, 'wb') as f:
        pickle.dump(vectorizer, f)

    print(f"Modelo salvo em: {caminho_modelo}")
    print(f"Vectorizer salvo em: {caminho_vectorizer}")


if __name__ == "__main__":
    CAMINHO_DADOS = "data/exemplo_tratado.csv"
    CAMINHO_MODELO = "models/modelo_classificador.pkl"
    CAMINHO_VECTORIZER = "models/tfidf_vectorizer.pkl"

    treinar_modelo(CAMINHO_DADOS, CAMINHO_MODELO, CAMINHO_VECTORIZER)
