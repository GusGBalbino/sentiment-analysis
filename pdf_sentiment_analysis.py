import os
import re
import pdfplumber
from textblob import TextBlob
from dotenv import load_dotenv
import concurrent.futures
import time

load_dotenv()

PDF_FOLDER_PATH = os.getenv('PDF_FOLDER_PATH')
MAX_WORKERS = int(os.getenv('MAX_WORKERS'))
POSITIVE_THRESHOLD = float(os.getenv('SENTIMENT_POSITIVE_THRESHOLD'))
NEGATIVE_THRESHOLD = float(os.getenv('SENTIMENT_NEGATIVE_THRESHOLD'))

def preprocess_text(text):

    '''
    Contextualiza moedas e percentuais e remove caracteres desnecessários e sem uso do texto recolhido.
    '''

    replacements = {
        'R\$': 'real ',
        '%': ' porcento ',
        '$': 'dólar ',
        '€': 'euro ',
        'UDM': 'unidade de medida ',
        'EBITDA': 'lucros antes de juros impostos depreciação e amortização',
        'ROIC': 'retorno sobre capital investido',
        'ROE': 'retorno sobre o patrimônio líquido',
        'Capex': 'despesas de capital'
    }

    for key, value in replacements.items():
        text = text.replace(key, value)
    
    text = re.sub(r'\b[a-zA-Z]\b', ' ', text)
    text = re.sub(r'[\+\-\*/\(\)\[\]\{\}\|\%\<\>\=]', ' ', text)
    text = re.sub(r'\b\d+\.?\d*\b', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def extract_text(pdf_path):

    '''
    Extração do texto dos PDFs.
    '''

    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ''
    return preprocess_text(text)

def analyze_sentiment(text):

    '''
    Análise do texto com TextBlob.
    '''

    blob = TextBlob(text)
    return blob.sentiment.polarity

def classify_sentiment(polarity):

    '''
    Análise da polaridade do texto
    '''

    if polarity < NEGATIVE_THRESHOLD:
        return 'Negativo'
    elif polarity > POSITIVE_THRESHOLD:
        return 'Positivo'
    else:
        return 'Neutro'

def process_pdf(pdf_path):

    '''
    Processamento do PDF, retornando os dados a respeito da análise.
    '''

    text = extract_text(pdf_path)
    polarity = analyze_sentiment(text)
    sentiment = classify_sentiment(polarity)
    return {'Nome do arquivo': os.path.basename(pdf_path), 'Polaridade': polarity, 'Sentimento': sentiment}

def analyze_pdf_folder(folder_path):

    '''
    Retorno do processo em forma de dicionários, categorizando os resultados.
    Utilização do Process Pool para tornar o módulo mais rápido e eficiente.
    '''

    results = {'Positivo': [], 'Neutro': [], 'Negativo': []}
    pdf_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.pdf')]
    
    start_time = time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_pdf = {executor.submit(process_pdf, pdf_path): pdf_path for pdf_path in pdf_paths}
        for future in concurrent.futures.as_completed(future_to_pdf):
            result = future.result()
            results[result['Sentimento']].append(result)
    total_time = time.time() - start_time
            
    return results, total_time

results, processing_time = analyze_pdf_folder(PDF_FOLDER_PATH)
for sentiment, files in results.items():
    print(f"\nSentimento: {sentiment}")
    for file in files:
        print(file)
print(f"\nTempo de processamento: {processing_time:.2f} segundos")
