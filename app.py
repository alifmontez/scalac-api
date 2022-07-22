from operator import truediv
from flask import Flask
from flask import jsonify
from urllib.request import urlopen
import json
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def base_url():
    """Base url to test API."""

    r = requests.get('http://bash.org.pl/text', stream=True)

    joke_count = 0
    joke = ""
    data = {}

    for line in r.iter_lines():
        line = str(line)[2:][:-1]

        if joke_count == 100:
            break

        if line != "%":
            joke += line + "\\n"
        else:
            data[joke_count] = joke
            joke_count+=1
            joke = ""

    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)