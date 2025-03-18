from rest_framework import serializers
from .models import Genre, Artist, Album, Track, Customer

class GenreSerializer(serializers.Serializer):
  name = serializers.CharField(max_length=100)

  def create(self, validated_data):
    return Genre(**validated_data).save()

class ArtistSerializer(serializers.Serializer):
  name = serializers.CharField(max_length=100)
  age = serializers.IntegerField()
  is_producer = serializers.BooleanField()
  place_of_birth = serializers.CharField(max_length=100)
  website = serializers.CharField(max_length=100, required=False)
  followers = serializers.IntegerField(required=False)

  def create(self, validated_data):
    return Artist(**validated_data).save()


class AlbumSerializer(serializers.Serializer):
  name = serializers.CharField(max_length=100) 
  release_date = serializers.DateTimeField()
  cover_art = serializers.URLField(max_length=100)

  def create(self, validated_data):
    return Album(**validated_data).save()

class TrackSerializer(serializers.Serializer):
  title = serializers.CharField(max_length=100)
  length = serializers.IntegerField()

  def create(self, validated_data):
    return Track(**validated_data).save()


class CustomerSerializer(serializers.Serializer):
  name = serializers.CharField(max_length=100)
  age = serializers.IntegerField()
  email = serializers.EmailField()

  def create(self, validated_data):
    return Customer(**validated_data).save()
