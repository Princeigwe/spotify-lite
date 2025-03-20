from django.shortcuts import render
from .models import Genre, Artist, Album, Track, Customer
from .serializers import GenreSerializer, ArtistSerializer, TrackSerializer, CustomerSerializer, AlbumReleaseSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from neomodel import DoesNotExist



class GenreList(APIView):

  def get(self, request):
    genres = Genre.nodes.all()
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)
  
  def post(self, request):
    serializer = GenreSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArtistList(APIView):
  
  def get(self, request):
    artists = Artist.nodes.all()
    serializer = ArtistSerializer(artists, many=True)
    return Response(serializer.data)
  
  def post(self, request):
    serializer = ArtistSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlbumReleaseList(APIView):
  
  def get(self, request):
    albums = Album.nodes.all()
    serializer = AlbumReleaseSerializer(albums, many=True)
    return Response(serializer.data)
  
  def post(self, request):
    serializer = AlbumReleaseSerializer(data=request.data)
    if serializer.is_valid():
      try:
        artist = Artist.nodes.get(name=serializer.validated_data['producer_name'])
        serializer.save()
        album = Album.nodes.get(name=serializer.validated_data['name'])
        artist.produced.connect(album)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      except DoesNotExist as e:
        return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)