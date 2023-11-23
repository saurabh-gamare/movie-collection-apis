import requests
from time import time
from base64 import b64encode
import os
from rest_framework.views import APIView
from rest_framework.response import Response


class MovieList(APIView):

    def basic_auth(self):
        username = os.environ.get('api_username')
        password = os.environ.get('api_password')
        token = b64encode(f'{username}:{password}'.encode('utf-8')).decode('ascii')
        return f'Basic {token}'

    def get(self, request):
        page = request.query_params.get('page')
        endpoint = 'http://demo.credy.in/api/v1/maya/movies'
        endpoint = f'{endpoint}?page={page}' if page else endpoint
        headers = {'Content-Type': 'application/json', 'Authorization': self.basic_auth()}
        response_data = {}
        start = time()
        while time() - start < 10:
            try:
                response = requests.get(endpoint, headers=headers, timeout=5)
                if response.status_code == 200 and response.json().get('results'):
                    response_data = response.json()
                    break
                else:
                    response_data = {}
            except:
                response_data = {}
        return Response(response_data)
