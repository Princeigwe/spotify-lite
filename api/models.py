from django.db import models
import neomodel
import datetime
import pytz


class Genre(neomodel.StructuredNode):
    name = neomodel.StringProperty(unique_index=True, required=True)
    
    track = neomodel.RelationshipTo('Track', 'HAS_TRACK')
    

class Artist(neomodel.StructuredNode):
    name = neomodel.StringProperty(unique_index=True, required=True)
    age = neomodel.IntegerProperty()
    is_producer = neomodel.BooleanProperty(default=False)
    place_of_birth = neomodel.StringProperty()
    website = neomodel.StringProperty()
    followers = neomodel.IntegerProperty()

    produced = neomodel.RelationshipTo('Album', 'PRODUCED')
    collaboed_with = neomodel.RelationshipTo('Artist', 'COLLABOED_WITH')
    sang_in = neomodel.RelationshipTo('Track', 'SANG_IN')


class Album(neomodel.StructuredNode):
    name = neomodel.StringProperty(unique_index=True, required=True)
    release_date = neomodel.DateTimeProperty(default=lambda: datetime.datetime.now(pytz.utc), index=True)
    cover_art = neomodel.StringProperty()

    has_track = neomodel.RelationshipTo('Track', 'HAS_TRACK')


class Track(neomodel.StructuredNode):
    title = neomodel.StringProperty(unique_index=True, required=True)
    length = neomodel.IntegerProperty()



class Customer(neomodel.StructuredNode):
    name = neomodel.StringProperty(unique_index=True, required=True)
    age = neomodel.IntegerProperty()
    email = neomodel.StringProperty()

    liked = neomodel.RelationshipTo('Track', 'LIKED')

