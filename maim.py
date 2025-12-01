from flask import Flask, render_template, jsonify, request
import requests
import random
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Конфигурация API
API_NINJAS_KEY = 'gHqZxH7sgINl/GoNDOjcuQ==OkUpUEf2ABpqQT1B'
API_ENDPOINTS = {
    'api_ninjas': 'https://api.api-ninjas.com/v1/quotes',
    'quoteslate': 'https://quoteslate.vercel.app/api/quotes/random'
}

# Запасные цитаты на случай недоступности API
FALLBACK_QUOTES = [
    {
        "quote": "Жизнь — это то, что с тобой происходит, пока ты строишь другие планы.",
        "author": "Джон Леннон",
        "category": "life"
    },
    {
        "quote": "Единственный способ сделать великую работу — любить то, что ты делаешь.",
        "author": "Стив Джобс",
        "category": "work"
    },
    {
        "quote": "Будь изменением, которое ты хочешь видеть в мире.",
        "author": "Махатма Ганди",
        "category": "inspiration"
    },
    {
        "quote": "Успех — это способность идти от неудачи к неудаче, не теряя энтузиазма.",
        "author": "Уинстон Черчилль",
        "category": "success"
    },
    {
        "quote": "Два самых важных дня в твоей жизни: день, когда ты появился на свет, и день, когда понял, зачем.",
        "author": "Марк Твен",
        "category": "wisdom"
    }
]


def get_api_ninjas_quote():
    """Получить цитату из API Ninjas"""
    try:
        headers = {'X-Api-Key': API_NINJAS_KEY} if API_NINJAS_KEY else {}
        response = requests.get(API_ENDPOINTS['api_ninjas'], headers=headers, timeout=5)

        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                quote_data = data[0]
                return {
                    'quote': quote_data.get('quote', ''),
                    'author': quote_data.get('author', 'Неизвестный автор'),
                    'category': quote_data.get('category', 'general'),
                    'source': 'API Ninjas'
                }
    except Exception as e:
        print(f"Ошибка API Ninjas: {e}")

    # Возвращаем случайную запасную цитату
    fallback = random.choice(FALLBACK_QUOTES)
    return {
        'quote': fallback['quote'],
        'author': fallback['author'],
        'category': fallback['category'],
        'source': 'API Ninjas (запасная)'
    }


def get_quoteslate_quote():
    """Получить цитату из QuotesLate"""
    try:
        response = requests.get(API_ENDPOINTS['quoteslate'], timeout=5)

        if response.status_code == 200:
            data = response.json()
            return {
                'quote': data.get('quote', ''),
                'author': data.get('author', 'Unknown Author'),
                'category': data.get('category', 'general'),
                'tags': data.get('tags', []),
                'source': 'QuotesLate'
            }
    except Exception as e:
        print(f"Ошибка QuotesLate: {e}")

    # Возвращаем случайную запасную цитату
    fallback = random.choice(FALLBACK_QUOTES)
    return {
        'quote': fallback['quote'],
        'author': fallback['author'],
        'category': fallback['category'],
        'source': 'QuotesLate (запасная)'
    }


@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')


@app.route('/get_quote')
def get_quote():
    """API endpoint для получения цитаты"""
    source = request.args.get('source', 'api_ninjas')

    if source == 'quoteslate':
        quote_data = get_quoteslate_quote()
    else:
        quote_data = get_api_ninjas_quote()

    return jsonify(quote_data)


@app.route('/get_both_quotes')
def get_both_quotes():
    """Получить цитаты из обоих источников"""
    quotes = {
        'api_ninjas': get_api_ninjas_quote(),
        'quoteslate': get_quoteslate_quote()
    }
    return jsonify(quotes)


if __name__ == '__main__':
    app.run(debug=True)