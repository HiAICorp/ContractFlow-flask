import os
import google.generativeai as genai
from pypdf import PdfReader
import csv 

def getTextFromPdf(path):
   
    reader = PdfReader(path)
    text = ""
    for pageNumber in reader.pages:
        text += pageNumber.extract_text()
    return text

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain"
}
print("Generation config:", generation_config)

model = genai.GenerativeModel(
  model_name="gemini-1.0-pro",
  generation_config=generation_config,
)
print("Model:", model)

def send_request_to_process(message):
  chat_session = model.start_chat(
    history=[]
  )
  prompt = "Generate a JSON response for a SOW with the following fields:Practice, End_date in DD-MM-YYYY format, Buyer, Seller, Agreement, Geo, Contract_Type, MSA_date in DD-MM-YYYY format, Start_date in DD-MM-YYYY format, Expiring_60, Amount (give the amount in numbers only no other special characters). If there is no value for any of the fields, then enter 'NULL' as value for the field, which is the key also the response should not be in markdown format"
  message = f"{message}\n\n{prompt}"
  response = chat_session.send_message(message)
  print("Response:", response.text)
  with open('response.csv', 'a', newline='') as csvfile:
    fieldnames = ['Practice', 'End_date', 'Buyer', 'Seller', 'Agreement', 'Geo', 'Contract_Type', 'MSA_date', 'Start_date', 'Expiring_60', 'Amount']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    if csvfile.tell() == 0:
      # Write the header only once
      writer.writeheader()

    # Write the response to the CSV file
    writer.writerow(eval(response.text))

  return response.text.replace("```json", "").replace("```", "")
 






