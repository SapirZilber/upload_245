from flask import Flask, render_template, url_for
from typing import Dict, List
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
        'x-rapidapi-key': "e57ee6c9d5mshcdc0eefc7c31f5cp11fc53jsn81cca60b7931"
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
        votes = movie["imdbVoteCount"]
        dict = {"title": title, "rating": rating, "year": year, "cast": cast, "description": description, "votes": votes}
        movies_details.append(dict)
    movies_details.sort(key=lambda x: x["votes"], reverse=True)
    return movies_details



