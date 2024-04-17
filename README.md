
# Análise de Sentimentos em Relatórios Financeiros PDF

Este projeto realiza a análise de sentimentos em documentos PDF contendo relatórios financeiros. O objetivo é classificar os sentimentos expressos nos textos como Positivo, Neutro ou Negativo.

## Funcionalidades

- Extração de texto de arquivos PDF.
- Pré-processamento de texto para remover dados não informativos e normalizar termos financeiros.
- Análise de sentimentos usando a biblioteca TextBlob.
- Classificação de sentimentos em três categorias: Positivo, Neutro e Negativo.

## Configuração

Para executar o projeto, é necessário configurar as seguintes variáveis de ambiente no arquivo `.env`:

```plaintext
PDF_FOLDER_PATH=/caminho/para/sua/pasta/de/pdf
MAX_WORKERS=8
SENTIMENT_POSITIVE_THRESHOLD=0.1
SENTIMENT_NEGATIVE_THRESHOLD=-0.1
```

## Dependências

- Python 3.10+

Instale as dependências com:

```bash
pip install -r requirements.txt
```

Após a instalação, é necessário preparar a TextBlob com:

```bash
python -m textblob.download_corpora
```

## Uso

Para executar a análise, coloque os PDFs desejados na pasta especificada em `PDF_FOLDER_PATH` e execute o script Python. 
Os resultados serão exibidos no console, incluindo a classificação de sentimentos para cada PDF e o tempo total de processamento.

Os PDFs utilizados para teste foram extraídos de: https://ri.simpar.com.br/central-de-resultados/

## Features Futuras

- Integrar o retorno dos dados ao PostgreSQL.
- Integrar a funcionalidade a uma API para receber o PDF.
