import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():

    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText()


@app.route('/')
def home():
    # Get a random fact as a string
    fact = get_fact()

    # Send the request to the pig latinizer
    urlReq = "https://hidden-journey-62459.herokuapp.com/piglatinize/"
    payload = {'input_text': fact}
    post_req = requests.post(urlReq, data=payload, allow_redirects=False)

    # Get the url where the response will come from
    urlResponse = post_req.headers['Location']

    # Get the response and pull the pig latin string from the headers
    response = requests.get(urlResponse)
    soup = BeautifulSoup(response.content, "html.parser")
    pigs = soup.find_all('h2')

    return pigs[0].nextSibling.strip()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)

