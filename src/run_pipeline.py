import src.data_preprocessing as data_preprocessing
import src.train_model as train_model

def main():

    print("Iniciando pré-processamento dos dados...")
    data_preprocessing.preprocessar_csv(caminho_entrada, caminho_limpo)

    print("Iniciando treinamento do modelo...")
    train_model.treinar_modelo(caminho_limpo, caminho_modelo, caminho_vectorizer)

    caminho_entrada = "data/exemplo.csv"  # CSV original, com colunas 'text' e 'label'
    caminho_limpo = "data/exemplo_tratado.csv"  # CSV após pré-processamento
    caminho_modelo = "models/modelo_classificador.pkl"
    caminho_vectorizer = "models/tfidf_vectorizer.pkl"

    print("Pipeline finalizado com sucesso!")


if __name__ == "__main__":
    main()
