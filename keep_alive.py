import http.client
import json
import os
import time
from threading import Thread

from flask import Flask

import CardHTML

app = Flask(__name__)

last = 0

def buid_html():
    global content
    global last
    
    if time.time() - last < 60:
        return "Wait 1 minute before refreshing"

    content = ("<!DOCTYPE html> <html lang=\"en\">"
               "<head>"
               "<meta charset=\"UTF-8\">"
               "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">"
               "<meta http-equiv=\"X-UA-Compatible\" content=\"ie=edge\">"
               "<title>HTML 5 Boilerplate</title>"
               "</head>"
               "<body>"
               "<h1 style=\"font-size: 50px;margin: 0;text-align: center;font-family: 'Manrope', sans-serif;font-weight: bold;\">" +
               os.environ['username'] + "</h1>"
               "<br> <br>")

    for channel in channels:
        cannel_id = channels_by_name(channel)

        content += (("<div style=\"padding: 20px;display: flex;flex-direction: column;gap: 20px;\"> <p "
                     "style=\"font-size: 40px;margin: 0;font-family: 'Manrope', sans-serif;font-weight: bold;\">")
                    + channel + ": " + get_points(cannel_id)
                    + "</p><div style=\"padding: 20px;display: "
                      "flex;width: 300px;flex-direction: row;gap: 20px;\">"
                    + get_cards(cannel_id) + "</div></div>")

    content += ("<script> function execute(channelId, id) {"
                "const myHeaders = new Headers();"
                "myHeaders.append(\"Authorization\", \"Bearer " + os.environ['STREAMELEMENTS_TOKEN'] + "\");"
                "const requestOptions = {"
                    "method: \"POST\","
                    "headers: myHeaders,"
                    "redirect: \"follow\""
                "};"
                
                "fetch('https://api.streamelements.com/kappa/v2/store/' + channelId + '/redemptions/' + id + '', requestOptions)"
                    ".then((response) => response.json())"
                    ".then((responseData) => {"
                        "const accessCode = getAccessCode(responseData);"
                            "if (accessCode) {"
                            "alert(accessCode);"
                            "console.log(accessCode);"
                            "} else {"
                            "console.log(responseData);"
                            "}"
                    "}).catch((error) => console.log(responseData));"
                "}"
                
                "function getAccessCode(responseData) {"
                    "if (responseData && typeof responseData === 'object' && responseData.hasOwnProperty('accessCode')) {"
                        "return responseData.accessCode;"
                    "} else {"
                        "alert('Couldnt extract code');"
                        "return null;"
                "}}</script></body></html>")

    last = time.time()

    return content


@app.route('/')
def index():
    buid_html()
    return content


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

    returnString = ""

    try:
        returnString = str(json.loads(data.decode("utf-8"))["points"])
    except:
        returnString = "-"

    return returnString


def get_cards(id):
    conn = http.client.HTTPSConnection("api.streamelements.com")

    headers = {
        'Accept': "application/json; charset=utf-8",
        'Authorization': "Bearer " + os.environ['STREAMELEMENTS_TOKEN']
    }

    conn.request("GET", "/kappa/v2/store/" + id + "/items?limit=0&offset=0", headers=headers)

    res = conn.getresponse()
    data = res.read()
    json_data = json.loads(data.decode("utf-8"))

    content = ""

    try:
        for card in json_data:
            if (card["enabled"] == False):
                continue

            content += (
                get_card_html(
                    card["name"],
                    card["description"],
                    card["thumbnail"],
                    card["_id"],
                    card["channel"])
            )
    except:
        print("couldn't get cards")

    return content


class Card:
    def __init__(self, title, src, id, channel_id):
        self.title = title
        self.src = src
        self.id = id
        self.channel_id = channel_id


def get_card_html(title, description, src, id, channel_id):
    return ("<div style=\"border-radius: 20px; background-color: rgb(208, 208, 208); padding: 20px;display: "
            "flex;width: 300px;flex-direction: column;gap: 20px;\">"
            + CardHTML.title_html(title)
            + CardHTML.description_html(description)
            + CardHTML.img_html(src)
            + CardHTML.button_html(id, channel_id)
            + "</div>")
