#Importa configurações do Django para acesso ao diretório de media
from django.conf import settings

#Importa bibliotecas auxiliares
import uuid # Para gerar nomes únicos de arquivos
import os # Para manipulação de caminhos de arquivos

# Leitura de PDFs
import fitz  
# Leitura de conteúdo da web
import urllib.request

#Tokenização de sentenças
import nltk
from nltk.tokenize import sent_tokenize

#PLN com Spacy
import spacy
nlp = spacy.load("pt_core_news_sm") #Carrega modelo de português do spaCy

#Cálculos numéricos
import numpy as np

# Parser HTML
import bs4 as bs

# Modelo de embedding de sentenças
from sentence_transformers import SentenceTransformer
#Similaridade de vetores
from sklearn.metrics.pairwise import cosine_similarity

#Geração de nuvem de palavras
from wordcloud import WordCloud
import matplotlib.pyplot as plt

#Downloads de recursos do NLTK
nltk.download('punkt')
nltk.download('punkt_tab')

#Expressões regulares
import re
 
#Carrega modelo multilingue para gerar vetores semânticos de setenças
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')


def carregar_texto(dados, tipo):
    if tipo == 'site':
        # lê e extrai texto de páginas web (somente os parágrafos <p>)
        texto_url = urllib.request.urlopen(dados)
        soup = bs.BeautifulSoup(texto_url, 'html.parser')
        paragrafos = soup.find_all('p')
        conteudo = ' '.join([p.get_text() for p in paragrafos])
        return conteudo
    elif tipo == 'arquivo':
         # Lê e extrai texto de arquivos PDF usando PyMuPDF
        try:
            doc = fitz.open(dados)
            conteudo = ""
            for page in doc:
                conteudo += page.get_text()
            doc.close()
            return conteudo

        except Exception as e:
            print(f"Erro em Pdf: {e}")
        except Exception as e:
            print(f"[Erro ao ler PDF] {e}")
            return ""

    
    else:
        print("Tipo inválido")

def preprocessamento(sentenca):
    # Remove espaços e transforma em minúsculas
    sentenca = sentenca.strip().lower()
    
    # Desconsidera sentenças muito curtas ou muito longas
    if len(sentenca) < 20 or len(sentenca) > 300:
        return False
    
    # Processa com spaCy
    doc = nlp(sentenca)

    # Mantém apenas sentenças com pelo menos um verbo
    if not any(token.pos_ == 'VERB' for token in doc):
        return False

    # Evita sentenças iniciadas por conectores vagos
    if re.match(r'^(isso|isto|aquilo|essa|esse|aquele|assim|desse modo|dessa forma)\b', sentenca):
        return False

    return True

def sumarizacao_gist(texto, idioma='portuguese', n_sentencas_min=25, proporcao=0.25):
    # Divide o texto em sentenças
    sentencas = sent_tokenize(texto, language=idioma)
    # Aplica filtro de pré-processamento
    sentencas_filtradas = [s for s in sentencas if preprocessamento(s)]
    
    if not sentencas_filtradas:
        return "Não foi possível identificar sentenças relevantes no texto."
    
    # Calcula número ideal de sentenças proporcional ao total (com mínimo de n_sentencas_min)
    total_sentencas = len(sentencas_filtradas)
    n_sentencas = max(n_sentencas_min, int(total_sentencas * proporcao))
    n_sentencas = min(n_sentencas, total_sentencas)  # nunca ultrapassa o total

    # Gera vetores de sentenças
    embedding = model.encode(sentencas_filtradas)

    # Matriz de similaridade entre todas as sentenças
    sim_matrix = cosine_similarity(embedding)

    # Calcula pontuação de cada sentença (soma das similaridades)
    scores = sim_matrix.sum(axis=1)

    # Identifica a sentença mais "central"
    idx_sentenca_principal = np.argmax(scores)
    
    # Pega as sentenças mais semelhantes à principal
    similaridades = sim_matrix[idx_sentenca_principal]
    indices_mais_proximas = np.argsort(similaridades)[-n_sentencas:]
    indices_mais_proximas.sort()  # Mantém a ordem original
    
    resumo = [sentencas_filtradas[i] for i in indices_mais_proximas]
    return ' '.join(resumo)


def gerar_nuvem_palavras(texto):
    # Define o caminho para salvar a nuvem de palavras
    pasta_clouds = os.path.join(settings.MEDIA_ROOT, 'clouds')

    # Nome único do arquivo
    nome_arquivo = f"nuvem_{uuid.uuid4().hex}.png"
    caminho_completo = os.path.join(pasta_clouds, nome_arquivo)
    
    # Processa o texto com spaCy
    doc = nlp(texto)

    # Filtra os lemas, removendo stopwords, pontuação e números
    palavras = [
        token.lemma_.lower()
        for token in doc
        if not token.is_stop and not token.is_punct and not token.like_num
    ]

    texto_limpo = " ".join(palavras)

    # Cria e salva a nuvem de palavras
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        collocations=False
    ).generate(texto_limpo)

    wordcloud.to_file(caminho_completo)

    # Retorna apenas o nome da imagem
    return nome_arquivo



def get_dados(tipo_entrada, url, arquivo):
    # Carrega o texto de acordo com o tipo de entrada (URL ou arquivo PDF)
    if tipo_entrada == 'url':
        texto = carregar_texto(url, tipo='site')
    elif tipo_entrada == 'file':
        texto = carregar_texto(arquivo, tipo='arquivo')
    else:
        raise ValueError("Tipo de entrada inválido. Use 'url' ou 'file'.")

    if not texto:
        return "Nenhum conteúdo encontrado.", None
    
    # Resume o texto com GistSumm e gera a nuvem
    resumo = sumarizacao_gist(texto)
    nome_imagem = gerar_nuvem_palavras(resumo)

    return resumo, nome_imagem

