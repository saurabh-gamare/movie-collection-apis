from rest_framework import serializers
from .models import Collection, Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True)

    class Meta:
        model = Collection
        fields = ['id', 'title', 'description', 'movies']

    def create(self, validated_data):
        movies = Movie.objects.filter(uuid__in=[details.get('uuid') for details in validated_data.get('movies')])
        collection_instance = Collection(title=validated_data.get('title'),
                                         description=validated_data.get('description'),
                                         user=validated_data.get('user'),
                                         collection_uuid=validated_data.get('collection_uuid'))
        collection_instance.save()
        for details in movies:
            collection_instance.movies.add(details)
        return collection_instance

    def update(self, collection_instance, validated_data):
        movies = Movie.objects.filter(uuid__in=[details.get('uuid') for details in validated_data.get('movies')])
        collection_instance.title = validated_data.get('title')
        collection_instance.description = validated_data.get('description')
        collection_instance.save()
        collection_instance.movies.clear()
        for details in movies:
            collection_instance.movies.add(details)
        return collection_instance


class RetrieveCollectionSerializer(serializers.ModelSerializer):
    uuid = serializers.CharField(source='collection_uuid')
    genres = serializers.StringRelatedField(source='movies', many=True)

    class Meta:
        model = Collection
        fields = ['title', 'description', 'uuid', 'genres']
