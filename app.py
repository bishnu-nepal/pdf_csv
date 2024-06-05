from flask import Flask, request, send_file, render_template, jsonify
import fitz  # PyMuPDF
import csv
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def pdf_to_csv(pdf_path, output_csv_path):
    try:
        # Open the PDF file
        document = fitz.open(pdf_path)
        
        # Initialize a list to hold text data
        text_data = []
        
        # Iterate through each page
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            text = page.get_text("text")
            text_data.extend(text.splitlines())
        
        # Write the text data to a CSV file
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as output_file:
            writer = csv.writer(output_file)
            for line in text_data:
                writer.writerow([line])
        return True, output_csv_path
    except Exception as e:
        print(f"Error: {e}")
        return False, str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['pdf']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.csv')
        
        file.save(input_path)
        success, result = pdf_to_csv(input_path, output_path)
        
        if success:
            return send_file(result, as_attachment=True, download_name='output.csv')
        else:
            return jsonify({'error': result}), 500

if __name__ == '__main__':
    app.run(debug=True)
