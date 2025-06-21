# Sumarização_GIST

O projeto **Sumarização_GIST** é uma aplicação para sumarização automática de documentos PDF e URLs, baseada no algoritmo Gist descrito na tese *“Comparativo entre o algoritmo de Luhn e o algoritmo GistSumm para sumarização de Documentos”* (Muller, Granatyr, Lessing, 2015).

O algoritmo Gist busca identificar a sentença que melhor expressa a ideia principal do texto e, a partir dela, seleciona outras sentenças relevantes para compor o resumo final. O sistema também inclui um gerador de nuvem de palavras (Word Cloud) para visualizar os termos mais importantes do resumo produzido.

---

## Funcionalidades

- Extração de texto de documentos PDF utilizando **PyMuPDF** (módulo `fitz`).
- Extração de conteúdo de páginas web (HTML) usando **BeautifulSoup** (`bs4`) com o parser `html.parser`.
- Processamento de linguagem natural em português com **NLTK** (tokenização de sentenças) e **spaCy** (modelo `pt_core_news_sm`).
- Operações numéricas e manipulação de vetores com **NumPy** (versão inferior a 2.0 para garantir compatibilidade).
- Representação semântica de sentenças via embeddings com **sentence-transformers**, utilizando o modelo multilingue `'paraphrase-multilingual-MiniLM-L12-v2'`.
- Cálculo de similaridade entre vetores com **scikit-learn** (`cosine_similarity`).
- Geração de nuvem de palavras a partir do resumo, utilizando **wordcloud** e visualização com **matplotlib**.
- Integração com **Django** para disponibilização da aplicação via web.

---

## Instalação e Configuração (Linux)

```bash
cd {caminho_do_projeto}
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m spacy download pt_core_news_sm
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

```
---

## Observações

- **O projeto foi testado em ambientes Linux.**

- **É recomendável utilizar a versão do NumPy abaixo da 2.0 para evitar incompatibilidades com módulos compilados; porém, essa dependência já está especificada no arquivo `requirements.txt` para instalação automática.**

- **Para mais detalhes sobre o algoritmo Gist, consulte a tese mencionada acima.**