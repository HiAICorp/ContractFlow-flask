from flask import Flask, request, jsonify
from file_extractor_api import getTextFromPdf, send_request_to_process
import os
import json

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

from flask import Flask, request, jsonify
import traceback

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    try:
        print("Request received")
        print("Form data:", request.form)
        print("Files:", request.files)

        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        print(f"File received: {file.filename}")
        file.save("./temp/contract_file.pdf")
        textFromPdf = getTextFromPdf("./temp/contract_file.pdf")
        res = send_request_to_process(textFromPdf)
        return jsonify({"result": json.loads(res)})

    except Exception as e:
        print("An error occurred:")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    if not os.environ.get("GEMINI_API_KEY"):
        raise ValueError("GEMINI_API_KEY environment variable is not set")
    app.run(debug=True)