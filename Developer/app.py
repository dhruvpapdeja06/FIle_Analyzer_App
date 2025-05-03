from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def upload_form():
    return '''
        <h2>Upload a .txt File for Analysis</h2>
        <form method="POST" action="/upload" enctype="multipart/form-data">
            <input type="file" name="file" accept=".txt">
            <input type="submit" value="Upload and Analyze">
        </form>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part in the request', 400

    file = request.files['file']
    
    if file.filename == '':
        return 'No file selected', 400

    if not file.filename.endswith('.txt'):
        return 'Only .txt files are allowed', 400

    text = file.read().decode('utf-8')
    words = text.split()
    word_count = len(words)
    from collections import Counter
    top_words = Counter(words).most_common(5)

    result = f"<h3>Analysis Results:</h3><p><b>Word Count:</b> {word_count}</p><b>Top 5 Words:</b><ul>"
    for word, freq in top_words:
        result += f"<li>{word}: {freq}</li>"
    result += "</ul>"

    return result

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
