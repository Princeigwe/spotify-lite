from django.urls import path
from . import views

urlpatterns = [
  path("genres/", views.GenreList.as_view()),
  path("artists/", views.ArtistList.as_view()),
  path("albums/", views.AlbumReleaseList.as_view()),
  path("albums/tracks/", views.AlbumTrackList.as_view()),
]