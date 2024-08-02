# Load packages
import openai # openai==0.28
import fitz  # PyMuPDF
import pandas as pd

# API-key
openai.api_key = ''

# Function from pdf to text
def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function text to ChatGPT
def analyze_text_gpt(text, query):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": "You concise as short as possible"},
            {"role": "user", "content": query + ": " + text}
        ],
        max_tokens=100
    )
    return response['choices'][0]['message']['content']

# Path of PDF
pdf_path = 'C:/Users/A/PycharmProjects/Jaarverslagen_SEO/2023-ING-Bank-NV-annual-report-pages-kort2.pdf'

# call function from pdf to text
pdf_text = extract_text(pdf_path)


# Queries
queries = {
    "name": "What is the name of the bank? Just report the name. I want you to report it as 'X' where X is the name of the bank",
    "turnover": "Give me the turnover of ING in 2023 in miljon of euro's, only the numerical value. I want you to report it as '€ X milion' Where X is the turnover value",
    "profit": "What is the profit of ING in 2023 in miljon of euro's, only the numerical value. I want you to report it as '€ X milion' Where X is the turnover value"
}

# Store results
results = {}

# Send queries through GPT-3
for key, query in queries.items():
    result = analyze_text_gpt(pdf_text, query)
    # Extract the relevant part from the response using regex or simple string operations
    if key == "name":
        results[key] = result.split("'")[0]  # Extracting the bank name
    else:
        results[key] = result.split("€ ")[0].split(" million")[0].strip()  # Extracting the numerical value

