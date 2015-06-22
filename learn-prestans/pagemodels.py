from google.appengine.ext import ndb

import prestans.ext.data.adapters
import prestans.ext.data.adapters.ndb

class Base(ndb.Model):
    
    @property
    def id(self):
        return self.key.id()


class Track(Base):
    name = ndb.StringProperty()

    @classmethod
    def make_key(self, band_id, album_id, request):
        track_key = Track(
            name=request.name, 
            parent=Album.get_by_key(band_id, album_id)
        )
        return track_key

    @classmethod
    def get_by_key(self, band_id, album_id, track_id):
        track_key = ndb.Key("Band", int(band_id), "Album", int(album_id), "Track", int(track_id))
        return track_key


class Album(Base):
    name = ndb.StringProperty()

    @classmethod
    def make_key(self, band_id, request):
        album_key = Album(
            name=request.name, 
            parent=Band.get_by_key(band_id)
        )
        return album_key

    @classmethod
    def get_by_key(self, band_id, album_id):
        album_key = ndb.Key("Band", int(band_id), "Album", int(album_id))
        return album_key


class Band(Base):
    name = ndb.StringProperty()
    #albums = ndb.KeyProperty(kind=Album, required=False, repeated=True)

    @classmethod
    def make_key(self, band_id):
        band_key = ndb.Key("Band", int(band_id))
        return band_key

    @classmethod
    def get_by_key(self, band_id):
        return self.make_key(band_id).get()