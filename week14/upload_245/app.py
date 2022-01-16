from flask import Flask, render_template, url_for
from typing import Dict, Iterator, List, Union
import requests
import json


API = "https://streaming-availability.p.rapidapi.com/search/basic"
STREAM_LIST = ["Netflix", "Prime", "Video", "Disney+", "HBO Max", "Hulu",
               "Peacock", "Paramount+", "Starz", "Showtime", "Apple TV+", "Mubi", "Stan", "Now", "Crave",
               "All 4", "iPlayer", "BritBox", "Hotstar", "Zee5", "Curiosity Stream"]


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html",
                           stream_list=STREAM_LIST)

@app.route("/<streaming>")
def stream_page(streaming: str):
    movies_raw = get_movies_from_stream(streaming)
    movies = get_movies_details(movies_raw)
    return render_template("stream_page.html",
                           streaming=streaming,
                           movies=movies)


def get_movies_from_stream(streaming: str) -> List[Dict]:
    querystring = {"country": "us", "service": streaming.lower(), "type": "movie", "output_language": "en",
                   "language": "en"}
    headers = {
        'x-rapidapi-host': "streaming-availability.p.rapidapi.com",
        'x-rapidapi-key': "API KEY"
    }
    response = requests.request("GET", API, headers=headers, params=querystring)
    movies_json = response.json()
    return movies_json["results"]


def get_movies_details(movies: List[Dict]) -> List[Dict]:
    movies_details = []
    for movie in movies:
        title = movie["title"]
        rating = movie["imdbRating"]
        year = movie["year"]
        description = movie["overview"]
        cast = movie["cast"]
        dict = {"title": title, "rating": rating, "year": year, "cast": cast, "description": description}
        movies_details.append(dict)
    return movies_details


app.run(debug=True)