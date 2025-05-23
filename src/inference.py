import pickle
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import re

nltk.download('punkt')
nltk.download('stopwords')

# Carrega modelo e vetorizador ao iniciar o script
with open('models/modelo_classificador.pkl', 'rb') as f:
    modelo = pickle.load(f)

with open('models/tfidf_vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

def preprocessar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r'\d+', '', texto)
    texto = texto.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(texto, language='portuguese')
    tokens = [t for t in tokens if t not in stopwords.words('portuguese')]
    return ' '.join(tokens)

def classificar_bloco(texto):
    texto_limpo = preprocessar_texto(texto)
    texto_vec = vectorizer.transform([texto_limpo])
    pred = modelo.predict(texto_vec)
    return pred[0]
