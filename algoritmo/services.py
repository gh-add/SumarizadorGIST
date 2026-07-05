from django.conf import settings #Importa configurações do Django 
import uuid # Para gerar nomes únicos de arquivos
import os # Para manipulação de caminhos de arquivos
import fitz  # Leitura de PDFs
from urllib.request import Request, urlopen# Leitura de conteúdo da web
from urllib.error import HTTPError, URLError # Tratamento de erros de requisição
import re #Expressões regulares
import numpy as np  #Cálculos numéricos
import bs4 as bs # Parser HTML beautiful soup
import logging # Para registro de logs
logger = logging.getLogger(__name__) # Configura logger para este módulo

from nltk.tokenize import sent_tokenize
from wordcloud import WordCloud #Geração de nuvem de palavras
from sklearn.metrics.pairwise import cosine_similarity #Similaridade de vetores

#Globais
_nlp = None
_model = None

# Lazy Loading (imports pesados)
def get_nlp():
        global _nlp 
        if _nlp is None:
            import spacy #PLN com Spacy
            _nlp = spacy.load("pt_core_news_sm") #Carrega modelo de português do spaCy
        return _nlp
    
def get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer # Modelo de embedding de sentenças
        _model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2') #Carrega modelo multilingue para gerar vetores semânticos de setenças
    return _model
    
def ensure_nltk():
     import nltk #Tokenização de sentenças
     nltk.download('punkt', quiet=True) #Downloads de recursos do NLTK
        

# Service
class GistSummService:

    def _carregar_texto(self, dados, tipo):
        # lê e extrai texto de páginas web (somente os parágrafos <p>)
        if tipo == 'url':
            if not dados:
                raise ValueError("URL não fornecida.")
            try:
                req = Request(dados, headers={'User-Agent': 'Mozilla/5.0'})  # Evita bloqueio por User-Agent
                response = urlopen(req)
                soup = bs.BeautifulSoup(response.read(), 'html.parser')
                paragrafos = soup.find_all('p')
                conteudo = ' '.join([p.get_text() for p in paragrafos])
                return conteudo
            except Exception as e:
                logger.exception(f"Erro ao carregar texto da URL {dados}: {e}")
            except HTTPError as e:
                logger.error(f"Erro HTTP ao acessar a URL {dados}: {e.code} - {e.reason}")
            except URLError as e:
                logger.error(f"Erro de URL ao acessar a URL {dados}: {e.reason}")
        # Lê e extrai texto de arquivos PDF usando PyMuPDF
        elif tipo == 'file':
            try:
                doc = fitz.open(dados)
                conteudo = ""
                for page in doc:
                    conteudo += page.get_text()
                doc.close()
                return conteudo
            except Exception as e:
                logger.exception(f"Erro ao carregar texto do arquivo {dados}: {e}")
        else:
            raise ValueError("Tipo de entrada inválido. Use 'url' ou 'file'.")

    def _preprocessamento(self, sentenca):
        sentenca = sentenca.strip().lower() # Remove espaços e transforma em minúsculas
        if len(sentenca) < 20 or len(sentenca) > 300: # Desconsidera sentenças muito curtas ou muito longas
            return False
        
        doc = get_nlp()(sentenca)  # Processa com spaCy
        if not any(token.pos_ == 'VERB' for token in doc):  # Mantém apenas sentenças com pelo menos um verbo
            return False

        if re.match(r'^(isso|isto|aquilo|essa|esse|aquele|assim|desse modo|dessa forma)\b', sentenca):  # Evita sentenças iniciadas por conectores vagos
            return False

        return True

    def _sumarizacao_gist(self, texto, idioma='portuguese', n_sentencas_min=25, proporcao=0.25):
        sentencas = sent_tokenize(texto, language=idioma)     # Divide o texto em sentenças
        sentencas_filtradas = [s for s in sentencas if self._preprocessamento(s)]     # Aplica filtro de pré-processamento
        
        if not sentencas_filtradas:
            logger.warning("Nenhuma sentença relevante encontrada no texto.")
        
        # Calcula número ideal de sentenças proporcional ao total (com mínimo de n_sentencas_min)
        total_sentencas = len(sentencas_filtradas)
        n_sentencas = max(n_sentencas_min, int(total_sentencas * proporcao))
        n_sentencas = min(n_sentencas, total_sentencas)  # nunca ultrapassa o total

        embedding = get_model().encode(sentencas_filtradas) # Gera vetores de sentenças
        sim_matrix = cosine_similarity(embedding)  # Matriz de similaridade entre todas as sentenças
        scores = sim_matrix.sum(axis=1)     # Calcula pontuação de cada sentença (soma das similaridades)
        idx_sentenca_principal = np.argmax(scores) # Identifica a sentença mais "central"
        
        # Pega as sentenças mais semelhantes à principal
        similaridades = sim_matrix[idx_sentenca_principal]
        indices_mais_proximas = np.argsort(similaridades)[-n_sentencas:]
        indices_mais_proximas.sort()  # Mantém a ordem original
        
        resumo = [sentencas_filtradas[i] for i in indices_mais_proximas]
        return ' '.join(resumo)

    def _gerar_nuvem_palavras(self, texto):
        pasta_clouds = os.path.join(settings.MEDIA_ROOT, 'clouds')     # Define o caminho para salvar a nuvem de palavras
        os.makedirs(pasta_clouds, exist_ok=True)  # Cria a pasta se não existir
        nome_arquivo = f"nuvem_{uuid.uuid4().hex}.png" # Nome único do arquivo
        caminho_completo = os.path.join(pasta_clouds, nome_arquivo)
        
        doc = get_nlp()(texto)   #Processa  o texto com spaCy
        palavras = [  # Filtra os lemas, removendo stopwords, pontuação e números
            token.lemma_.lower()
            for token in doc
            if not token.is_stop and not token.is_punct and not token.like_num
        ]
        texto_limpo = " ".join(palavras)

        # Cria e salva a nuvem de palavras
        wordcloud = WordCloud(
            width=400,
            height=800,
            background_color='white',
            collocations=False
        ).generate(texto_limpo)
        wordcloud.to_file(caminho_completo)

        return nome_arquivo  # Retorna apenas o nome da imagem


    def __call__(self, tipo_entrada, url=None, arquivo=None):
        # Carrega o texto de acordo com o tipo de entrada (URL ou arquivo PDF)
        if tipo_entrada == 'url':
            texto = self._carregar_texto(url, tipo=tipo_entrada)
        elif  tipo_entrada == "file":
            texto = self._carregar_texto(arquivo, tipo=tipo_entrada)
        else:
            raise ValueError("Tipo de entrada inválido. Use 'url' ou 'file'.")

        if not texto:
            logger.warning("Nenhum texto encontrado.")
            return None, None

        # Resume o texto com GistSumm e gera a nuvem
        resumo = self._sumarizacao_gist(texto)
        nome_imagem = self._gerar_nuvem_palavras(resumo)

        return resumo, nome_imagem

