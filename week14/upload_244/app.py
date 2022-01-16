from flask import Flask, render_template, url_for
from typing import Dict, Iterator, List, Union
import json


WOLT_REST = r"C:\Users\sapirz\Desktop\PYTHON\week14\venv\upload_244\results.json"


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html",
                           header="Welcome to Wolt's Index")


@app.route("/restaurants/all")
def get_all_restaurants():
    rests_raw = get_rests(WOLT_REST)
    rests = get_rest_details(rests_raw)
    return render_template("restaurants.html",
                           header="All Restaurants",
                           restaurants=rests)


@app.route("/restaurants/open")
def get_open_restaurants():
    restaurants = get_rests(WOLT_REST)
    open_rests = list(does_deliver(restaurants))
    rests = get_rest_details(open_rests)
    return render_template("restaurants.html",
                           header="Open Restaurants",
                           restaurants=rests)


def get_rests(path: str) -> List[Dict[str, Union[str, Dict, List]]]:
    rests_dict = read_json(path)
    return rests_dict["sections"][0]["items"]


def read_json(path: str) -> Dict[str, Union[str, Dict, List]]:
    with open(path) as rests_results:
        return json.load(rests_results)


def get_rest_details(restaurants: List[Dict[str, Union[str, Dict, List]]]) -> List[Dict]:
    rests_details = []
    for rest in restaurants:
        name = rest["title"]
        categories = rest["filtering"]["filters"][0]["values"]
        if "rating" in rest["venue"].keys():
            score = rest["venue"]["rating"]["score"]
        else:
            score = -1
        dict = {"title": name, "categories": categories, "score": score}
        rests_details.append(dict)
    return rests_details


def does_deliver(restaurants: List[Dict[str, Union[str, Dict, List]]]) -> Iterator:
    for rest in restaurants:
        if rest["venue"]["delivers"] or "overlay" in rest.keys() and rest["overlay"]:
            yield rest


app.run(debug=True)

