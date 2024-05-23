from flask import request, jsonify
import requests
from  stopWords import stop_words
from datetime import datetime, timedelta
import os



api_key = os.getenv("API_KEY")

def get_news_title(title, date):
    try:
        
        # quitamos stop words
        filtered_title = ' '.join([word for word in title.split() if word not in stop_words])

        # ordenamos las palabras por longitud
        title_ordered_by_len = sorted(filtered_title.split(), key=len, reverse=True)
        if(len(title_ordered_by_len) > 5): title_ordered_by_len = title_ordered_by_len[0:3]
        title_with_and = ' AND '.join([word for word in title_ordered_by_len if word not in stop_words])

        exact_title_url = f"https://newsapi.org/v2/everything?searchIn=title&q="
        exact_title_url += f"{title_with_and}&page=1&language=es&apiKey={api_key}"
        today = datetime.today().date()

        # restamos 30 dias a la fecha de hoy
        date_limit = today - timedelta(days=30)
        
        if(date):
            if((date - timedelta(days=7)) > date_limit):
                date_limit = date - timedelta(days=7)
        
        exact_title_url = f"https://newsapi.org/v2/everything?searchIn=title&from={date_limit}"
        exact_title_url += f"&q={title_with_and}&page=1&language=es&apiKey={api_key}"
        exact_response = requests.get(exact_title_url)
        final_result = []

        # extraemos las fuentes        
        data = exact_response.json()
        print(len(data['articles']))
        for i in range(len(data['articles'])):
            article = data['articles'][i]
            final_result.append(article['source']['name']) 
            
        final_result = list(set(final_result))
        return final_result
        

    except Exception as e:
        print(e)
        return e



# def get_news_title2(title, date):
#     try:
        

        
#         exact_title_url = f"https://newsapi.org/v2/everything?searchIn=title&q={title}&page=1&language=es&apiKey={api_key}"
#         if(date): exact_title_url = f"https://newsapi.org/v2/everything?searchIn=title&from={date}&q={title}&page=1&language=es&apiKey={api_key}"
#         exact_response = requests.get(exact_title_url)
#         final_result = []
#         if exact_response:
#             data = exact_response.json()
#             print(len(data['articles']))
#             for i in range(len(data['articles'])):
#                 article = data['articles'][i]
#                 final_result.append(article['source']['name']) 
                
#             final_result = list(set(final_result))
#             return final_result
#         else:
#             converted_string = title
#             if len(converted_string) > 1:
#                 converted_string = converted_string.replace(' ', ' AND ')
#             title_containing_url = f"https://newsapi.org/v2/everything?searchIn=title&q={converted_string}&page=1&language=es&apiKey={api_key}"
#             containing_response = requests.get(title_containing_url)
#             data = containing_response.json()
#             return data

#     except Exception as e:
#         print(e)
#         return e

