from django.shortcuts import render
from .models import Genre, Artist, Album, Track, Customer
from .serializers import GenreSerializer, ArtistSerializer, AlbumSerializer, TrackSerializer, CustomerSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



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