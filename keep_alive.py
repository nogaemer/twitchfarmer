import os
import this

from flask import Flask, render_template
from threading import Thread
import http.client
import json

app = Flask(__name__)


@app.route('/')
def index():
    content = ""
    for channel in channels:
        content += "<p>" + channel + ": " + get_points(channels_by_name(channel)) + "</p>"

    return "<div style=\"display: flex;flex-direction: column;\">" + content + "</div>"


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive(channelss):
    global channels
    channels = channelss

    t = Thread(target=run)
    t.start()


def channels_by_name(name):
    conn = http.client.HTTPSConnection("api.streamelements.com")

    headers = {
        'Accept': "application/json; charset=utf-8",
        'Authorization': "Bearer " + os.environ['STREAMELEMENTS_TOKEN']
    }

    conn.request("GET", "/kappa/v2/channels/" + name, headers=headers)

    res = conn.getresponse()
    data = res.read()

    return json.loads(data.decode("utf-8"))["_id"]


def get_points(id):
    conn = http.client.HTTPSConnection("api.streamelements.com")

    headers = {
        'Accept': "application/json; charset=utf-8",
        'Authorization': "Bearer " + os.environ['STREAMELEMENTS_TOKEN']
    }

    conn.request("GET", "/kappa/v2/points/" + id + "/" + os.environ['username'], headers=headers)

    res = conn.getresponse()
    data = res.read()

    return str(json.loads(data.decode("utf-8"))["points"])
