from flask import Flask, request
from resolvers.get import get_news_title
from resolvers.post import clean_html, process_html
import asyncio
from flask_cors import CORS  # Import CORS from flask_cors

app = Flask(__name__)
CORS(app)

@app.route('/getNewsTitle', methods=['GET'])
def news_title():
    return get_news_title()

@app.route('/process_html', methods=['POST'])
def process_html_route():
    try:
        data = request.get_json()
        result = asyncio.run(process_html(data))
        return result
    except Exception as e:
        print(e)
        return "Internal Server Error", 500

@app.route('/clean_html', methods=['POST'])
def clean_html_content():
    try:
        data = request.get_json()
        html = data.get('html')
        if not html:  # HTML missing
            return "HTML missing", 400
        return clean_html(html)
    except Exception as e:
        print(e)
        return "Internal Server Error", 500
    
if __name__ == '__main__':
    app.run(debug=True)


