from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse

from engine import SearchEngine

import requests

from pathlib import Path
from dotenv import load_dotenv
import os


load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

SECRET_KEY = os.getenv('SECRET_KEY')
URL = os.getenv('URL')
IP = os.getenv('IP')
PORT = int(os.getenv('PORT'))


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = SECRET_KEY
engine = SearchEngine(URL, 'engine/stop_words.txt', 'engine/robots.txt')

parser = reqparse.RequestParser()
parser.add_argument('new_url', required=True, type=str)


class SearchApi(Resource):
    def get(self, text):
        return jsonify(engine.handle_query(text))


class ChangeUrl(Resource):
    def post(self):
        args = parser.parse_args()
        new_url = args['new_url']
        try:
            request = requests.get(new_url)
        except:
            return jsonify({"message": "Error"})
        engine.change_url(new_url)
        return jsonify({"message": "Successful"})

    def get(self):
        return jsonify(engine.parser.main_url)


api.add_resource(SearchApi, '/api/search/<string:text>')
api.add_resource(ChangeUrl, '/api/change')


if __name__ == '__main__':
    app.run(port=PORT, host=IP)
