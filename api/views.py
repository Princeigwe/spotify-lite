from django.shortcuts import render
from .models import Genre, Artist, Album, Track, Customer
from .serializers import GenreSerializer, ArtistSerializer, AlbumReleaseSerializer, AlbumTrackSerializer,TrackSerializer, CustomerSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from neomodel import DoesNotExist, db



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
        serializer.save()
        artist = Artist.nodes.get(name=serializer.validated_data['producer_name'])
        album = Album.nodes.get(name=serializer.validated_data['name'])
        artist.produced.connect(album)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      except DoesNotExist as e:
        return Response({"error": f"{e}"}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlbumTrackList(APIView):
  def get(self, request):
    tracks = Track.nodes.all()
    serializer = AlbumTrackSerializer(tracks, many=True)
    return Response(serializer.data)
  
  def post(self, request):
    serializer = AlbumTrackSerializer(data=request.data)
    if serializer.is_valid():
      try:
        serializer.save()
        album = Album.nodes.get(name=serializer.validated_data['album_name'])
        genre = Genre.nodes.get(name=serializer.validated_data['genre_name'])
        track = Track.nodes.get(title = serializer.validated_data['title'])
        album.has_track.connect(track)
        genre.has_track.connect(track)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      except DoesNotExist as e:
        return Response({"error": f"{e}"}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TrackList(APIView):
  def get(self, request):
    tracks = Track.nodes.all()
    serializer = TrackSerializer(tracks, many=True)
    return Response(serializer.data)
  
  def post(self, request):
    serializer = TrackSerializer(data=request.data)
    if serializer.is_valid():
      try:
        serializer.save()
        producer = Artist.nodes.get(name=serializer.validated_data['producer_name'], is_producer=True)
        singer = Artist.nodes.get(name=serializer.validated_data['singer_name'], is_producer=False)
        album = Album.nodes.get(name=serializer.validated_data['album_name'])
        track = Track.nodes.get(title=serializer._validated_data['title'])
        genre = Genre.nodes.get(name=serializer.validated_data['genre_name'])

        album.has_track.connect(track)
        producer.collaboed_with.connect(singer)
        singer.sang_in.connect(track)
        genre.has_track.connect(track)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      except DoesNotExist as e:
        return Response({"error": f"{e}"}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TrackView(APIView):
  def delete(self, request, title):
    query = " MATCH (track: Track{ title: $title }) DETACH DELETE track; "
    db.cypher_query(query=query, params={"title":title} )
    return Response(status=status.HTTP_204_NO_CONTENT)