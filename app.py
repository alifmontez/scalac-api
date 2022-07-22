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

    first_line = True
    id = 0

    joke_count = 0
    joke = []
    data = {}
    sub_data = {}

    for line in r.iter_lines():

        line = line.decode('utf-8')

        if joke_count == 100:
            break

        if line != "%":
            if first_line:
                id = line[1:8]
                first_line = False
            else:
                joke.append(line)
        else:
            sub_data['url'] = "http://bash.org.pl/" + id
            sub_data['joke'] = joke
            data[id] = sub_data
            joke_count+=1
            joke = []
            sub_data = {}
            first_line = True

    response = app.response_class(
        response=json.dumps(data, indent=4, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)