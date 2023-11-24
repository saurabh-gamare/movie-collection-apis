import requests
from time import time
from base64 import b64encode
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CollectionSerializer, MovieSerializer, RetrieveCollectionSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Movie, Collection
from rest_framework import exceptions
import uuid
from collections import Counter


class MovieList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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


class MovieCollection(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_top_genres(self, genres):
        counts = Counter(genres)
        top_3_genres = counts.most_common(3)
        return top_3_genres

    def post(self, request):
        for details in request.data.get('movies'):
            movie_serializer = MovieSerializer(data=details)
            if movie_serializer.is_valid():
                Movie.objects.get_or_create(**details)
        collection_serializer = CollectionSerializer(data=request.data)
        if not collection_serializer.is_valid():
            raise exceptions.ValidationError({'error': collection_serializer.errors})
        collection_uuid = str(uuid.uuid4())
        collection_serializer.save(user=request.user, collection_uuid=collection_uuid)
        return Response({'collection_uuid': collection_uuid})

    def get(self, request):
        collections = Collection.objects.filter(user=request.user.id)
        serializer = RetrieveCollectionSerializer(collections, many=True)
        genres = []
        for details in serializer.data:
            genres.extend(details.pop('genres'))
        top3_genres = [details[0] for details in self.get_top_genres(genres)]
        data = {'collections': serializer.data, 'favourite_genres': top3_genres}
        return Response({'is_success': True, 'data': data})


class UpdateDeleteMovieCollection(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, uuid):
        for details in request.data.get('movies'):
            movie_serializer = MovieSerializer(data=details)
            if movie_serializer.is_valid():
                Movie.objects.get_or_create(**details)
        try:
            collection_instance = Collection.objects.get(collection_uuid=uuid)
        except:
            raise exceptions.ValidationError({'error': 'Invalid uuid'})
        collection_serializer = CollectionSerializer(collection_instance, data=request.data)
        if not collection_serializer.is_valid():
            raise exceptions.ValidationError({'error': collection_serializer.errors})
        collection_serializer.save()
        return Response(request.data)

    def delete(self, request, uuid):
        try:
            collection_instance = Collection.objects.get(collection_uuid=uuid)
        except:
            raise exceptions.ValidationError({'error': 'Invalid uuid'})
        collection_instance.delete()
        return Response({'collection_uuid': uuid})
