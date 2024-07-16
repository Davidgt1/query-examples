import requests
import json
from dotenv import load_dotenv
import os


load_dotenv()

api_key = os.getenv('API_KEY')
url_subgraph = os.getenv('URL_SUBGRAPH')
id_subgraph = os.getenv('ID_SUBGRAPH')
filepath_json = os.getenv('FILEPATH')


class GraphAPI:
    
    def __init__(self, api_key, url_subgraph, id_subgraph, filepath_json):
        self.api_key = api_key
        self.url_subgraph = url_subgraph
        self.id_subgraph = id_subgraph
        self.filepath_json = filepath_json
        self._validate_env_variables()

    def _validate_env_variables(self):

        if not self.api_key:
            raise Exception("API_KEY not found in .env file")
        if not self.url_subgraph:
            raise Exception("URL_SUBGRAPH not found in .env file")
        if not self.id_subgraph:
            raise Exception("ID_SUBGRAPH not found in .env file")

    def _read_query_from_json(self):

        with open(self.filepath_json) as file:
            query = json.load(file)['query']
        return query

    def _send_query(self, query):

        url = f'https://gateway-{self.url_subgraph}/api/{self.api_key}/subgraphs/id/{self.id_subgraph}'
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.post(url, json={'query': query}, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data['data']
        else:
            raise Exception(f"Query failed to run with a {response.status_code}: {response.text}")

    def query_graph_api(self):
        
        query = self._read_query_from_json()
        data = self._send_query(query)
        return data


graph_api = GraphAPI(api_key, url_subgraph, id_subgraph, filepath_json)
data = graph_api.query_graph_api()
print(data)
