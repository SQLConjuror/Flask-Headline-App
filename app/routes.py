from flask import Flask, render_template, flash, redirect, url_for, request, make_response
from app import app
import feedparser
import json
from urllib.request import urlopen
from urllib.request import quote
import datetime


RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}

DEFAULTS = {'publication':'bbc', 
            'city': 'London,UK', 
            'currency_from':'GBP',
            'currency_to':'USD'
            }

CURRENCY_URL="https://openexchangerates.org//api/latest.json?app_id=d332b5ba48ed404d82bfda1dd98f7072"

# @app.route("/")
# @app.route("/<publication>")
# def bbc():
#     return get_news(publication='bbc')

# @app.route("/cnn")
# def bbc():
#     return get_news(publication='cnn')

# @app.route("/")
# @app.route("/<publication>")
# def get_news(publication='bbc'):
#     feed = feedparser.parse(RSS_FEEDS[publication])
#     first_article = feed['entries'][0]
#     return render_template("home.html", articles=feed['entries'])



@app.route("/", methods=['GET', 'POST'])
def home():
    # get customized headlines, based on user input or default
    publication = get_value_with_fallback('publication')
    articles = get_news(publication)

    # get customized weather based on user input or default
    city = get_value_with_fallback('city')
    weather = get_weather(city)

    # get customized currency based on user input of default 
    currency_from = get_value_with_fallback("currency_from")
    currency_to = get_value_with_fallback("currency_to")
    rate, currencies = get_rate(currency_from, currency_to)

    # save cookies and return template
    response = make_response(render_template("home.html", articles=articles, weather=weather, currency_from=currency_from, currency_to=currency_to, rate=rate, currencies=sorted(currencies)))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)
    return response


def get_news(query):
    # query = request.args.get("publication")
    # Vquery = request.form.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']
    # weather = get_weather("London,UK")
    # return render_template("home.html", articles=feed['entries'],weather=weather)


def get_weather(query):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=bcf58fe4b14e0d738dda6e2bf3871500"
    query = quote(query)
    url = api_url.format(query)
    data = urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description":
                    parsed["weather"][0]["description"],
                    "temperature":parsed["main"]["temp"],
                    "city":parsed["name"],
                    'country': parsed['sys']['country']
                  }
    return weather
    

def get_rate(frm, to):
    all_currency = urlopen(CURRENCY_URL).read()
    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return (to_rate / frm_rate, parsed.keys())


def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
        return DEFAULTS[key]

