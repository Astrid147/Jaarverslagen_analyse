# Load packages
import os

import openai  # openai==0.28
import fitz  # PyMuPDF
import pandas as pd
import credentials


# Set your OpenAI API key
openai.api_key = credentials.api_key

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
            {"role": "system", "content": "You are a financial analist. you analyse reports. In what you do you are as concise and short as possible."},
            {"role": "user", "content": query + ": " + text}
        ],
        max_tokens=20
    )
    return response['choices'][0]['message']['content']

# Path of pdf directory
pdf_directory = 'C:/Users/AstridLensink/PycharmProjects/Jaarverslagen_SEO/RvC/eerstebatch'

# Queries
queries = prompts = {
    "name": "What is the name of the organisation? Just report the name. I want you to only report the name of the organisation. An example of the structure is 'ING Group",
    "year": "Please provide only the year of the report, with no additional text"
}


# List to store results
all_results = []

# Loop over each PDF in directory
for filename in os.listdir(pdf_directory):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_directory, filename)

        # Extract PDF
        pdf_text = extract_text(pdf_path)

        results = {
            "name": "",
            "year": "",
            "filename": filename
        }

        # Send through GPT
        for key, query in queries.items():
            result = analyze_text_gpt(pdf_text, query)
            results[key] = result.strip()

        # add to list of results
        all_results.append(results)

# Convert results to a DataFrame
df = pd.DataFrame(all_results)

# Save DataFrame to CSV
df.to_csv('AEX_data.csv', index=False)

