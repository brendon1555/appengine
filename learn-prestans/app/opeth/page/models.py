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
    def make_key(self, band_id, album_id, track_id):
        track_key = ndb.Key("Band", int(band_id), "Album", int(album_id), "Track", int(track_id))
        return track_key

    @classmethod
    def get_by_key(self, band_id, album_id, track_id):
        return self.make_key(band_id, album_id, track_id).get()


class Album(Base):
    name = ndb.StringProperty()

    @classmethod
    def make_key(self, band_id, album_id):
        album_key = ndb.Key("Band", int(band_id), "Album", int(album_id))
        return album_key

    @classmethod
    def get_by_key(self, band_id, album_id):
        return self.make_key(band_id, album_id).get()


class Band(Base):
    name = ndb.StringProperty()

    @classmethod
    def make_key(self, band_id):
        band_key = ndb.Key("Band", int(band_id))
        return band_key

    @classmethod
    def get_by_key(self, band_id):
        return self.make_key(band_id).get()