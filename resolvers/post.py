from flask import request, jsonify
from bs4 import BeautifulSoup
from resolvers.get import get_news_title
from utils.process_title import process_title
from utils.process_article import process_article



date_refs = {
    'ene': '01',
    'feb': '02',
    'mar': '03',
    'abr': '04',
    'may': '05',
    'jun': '06',
    'jul': '07',
    'ago': '08',
    'sep': '09',
    'oct': '10',
    'nov': '11',
    'dic': '12'
}
# Parse time to dd-mm-yyyy format


async def process_html(data):
    try:
       
        html = data.get('html')

        if not html:  # HTML missing
            return "HTML missing", 400

        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('title').text if soup.find('title') else ""
        h1 = soup.find('h1').text if soup.find('h1') else ""
        h2 = soup.find('h2').text if soup.find('h2') else ""

        p_tags = soup.find_all('p')

        # Concatenate the contents of <p> tags into a variable
        p = ''.join([p.get_text() for p in p_tags])
        # p = soup.find('p').text if soup.find('p') else ""
        article = soup.find('article').text if soup.find('article') else ""
        
        # Classify the article
        classification = "no classification available"
        if(p):
            # cleaned_article = clean_html(article)
            result = process_article(p)
            classification = "TRUE NEW" if result else "FAKE NEW"
            with open('p.txt', 'w') as f:
                f.write(p)
        elif(article):
            # cleaned_article = clean_html(article)
            result = process_article(article)
            classification = "TRUE NEW" if result else "FAKE NEW"
        
        # Classify the title
        title_classification = "no classification available"
        if(title):
            result = process_title(title)
            title_classification = result

        time = soup.find('time').text if soup.find('time') else ""
        if(len(time) > 0):
            time = time[:-12]
            time = time.split(' ')
            time[1] = date_refs[time[1]]
            time = '-'.join(time)
        
        sources = get_news_title(title, time)
        sources_string = ', '.join(sources)
        return_event = {
            "title": title,
            "h1": h1,
            "h2": h2,
            "article": article,
            "p": p,
            "article_classification": classification,
            "title_classification": title_classification,
            "sources": sources_string
        }

        response = jsonify(return_event)
        response.headers.set('Access-Control-Allow-Origin', '*')  
        return response, 200

    except Exception as e:
        print(e)
        return "Internal Server Error", 500

def clean_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    response = jsonify(soup.get_text())
    response.headers.set('Access-Control-Allow-Origin', '*')  
    return response, 200
