import prestans.rest
import prestans.http
import prestans.parser
import prestans.types
import prestans.provider.auth
import prestans.ext.appengine
import prestans.ext.data.adapters.ndb

import opeth.rest.models
import opeth.page.models
import opeth.rest.adapters

from google.appengine.api import users

#Prestans
class Base(prestans.rest.RequestHandler):
    __provider_config__ = prestans.provider.Config(
        authentication=prestans.ext.appengine.AppEngineAuthContextProvider()
    )


class LoginHandler(Base):

    def get(self):
        user = users.get_current_user()
        self.redirect(users.create_login_url('/api/band'))


class LogoutHandler(Base):
    
    def get(self):
        user = users.get_current_user()
        self.redirect(users.create_logout_url("/api/band"))


class RestBandCollectionHandler(Base):

    __parser_config__ = prestans.parser.Config(
        GET=prestans.parser.VerbConfig(
            response_attribute_filter_default_value=True,
            response_template=prestans.types.Array(element_template=opeth.rest.models.Band())
        ),
        POST=prestans.parser.VerbConfig(
            body_template=opeth.rest.models.Band(),
            response_template=None
        )
    )

    def get(self):
        #self.logger.error("hello from get")
        bands = opeth.page.models.Band.query()
        
        self.response.body = prestans.ext.data.adapters.ndb.adapt_persistent_collection(
            bands,
            opeth.rest.models.Band
        )
        self.response.status = prestans.http.STATUS.OK
   
    @prestans.provider.auth.login_required
    def post(self):
        #self.logger.error("hello from post")
        request = self.request.parsed_body
        band = opeth.page.models.Band(
            name=request.name
        )
        band.put()
        self.response.status = prestans.http.STATUS.NO_CONTENT


class RestBandEntityHandler(Base):

    __parser_config__ = prestans.parser.Config(
        GET=prestans.parser.VerbConfig(
            response_attribute_filter_default_value=True,
            response_template=opeth.rest.models.Band()
        )
    )

    def get(self, band_id):
        band = opeth.page.models.Band.get_by_key(band_id)
        if band is None:
            raise prestans.exception.NotFound("Band")
        
        self.response.http_status = prestans.http.STATUS.OK
        self.response.body = opeth.rest.models.Band(name=band.name)

    @prestans.provider.auth.login_required
    def delete(self, band_id):
        band = opeth.page.models.Band.get_by_key(band_id)
        if band is None:
            raise prestans.exception.NotFound("Band")

        opeth.page.models.ndb.delete_multi(opeth.page.models.ndb.Query(ancestor=band.key).iter(keys_only=True))


class RestAlbumCollectionHandler(Base):

    __parser_config__ = prestans.parser.Config(
        GET=prestans.parser.VerbConfig(
            response_attribute_filter_default_value=True,
            response_template=prestans.types.Array(element_template=opeth.rest.models.Album())
        ),
        POST=prestans.parser.VerbConfig(
            body_template=opeth.rest.models.Album(),
            response_template=None
        )
    )

    def get(self, band_id):
        band = opeth.page.models.Band.get_by_key(band_id)
        if band is None:
            raise prestans.exception.NotFound("Band")

        self.response.status = prestans.http.STATUS.OK
        self.response.body = prestans.ext.data.adapters.ndb.adapt_persistent_collection(
            opeth.page.models.Album.query(ancestor=band.key).fetch(),
            opeth.rest.models.Album
        )

    @prestans.provider.auth.login_required
    def post(self, band_id):
        request = self.request.parsed_body
        band = opeth.page.models.Band.get_by_key(band_id)
        album = opeth.page.models.Album(
            name=request.name, 
            parent=band.key
        )
        album.put()
        self.response.status = prestans.http.STATUS.NO_CONTENT


class RestAlbumEntityHandler(Base):

    __parser_config__ = prestans.parser.Config(
        GET=prestans.parser.VerbConfig(
            response_attribute_filter_default_value=True,
            response_template=opeth.rest.models.Album()
        )
    )

    def get(self, band_id, album_id):
        album = opeth.page.models.Album.get_by_key(band_id, album_id)
        if album is None:
            raise prestans.exception.NotFound("Album")
        
        self.response.http_status = prestans.http.STATUS.OK
        self.response.body = opeth.rest.models.Album(name=album.name)

    @prestans.provider.auth.login_required
    def delete(self, band_id, album_id):
        album = opeth.page.models.Album.get_by_key(band_id, album_id)
        if album is None:
            raise prestans.exception.NotFound("Album")
        opeth.page.models.ndb.delete_multi(opeth.page.models.ndb.Query(ancestor=album.key).iter(keys_only=True))


class RestTrackCollectionHandler(Base):

    __parser_config__ = prestans.parser.Config(
        GET=prestans.parser.VerbConfig(
            response_attribute_filter_default_value=True,
            response_template=prestans.types.Array(element_template=opeth.rest.models.Track())
        ),
        POST=prestans.parser.VerbConfig(
            body_template=opeth.rest.models.Track(),
            response_template=None
        )
    )

    def get(self, band_id, album_id):
        album = opeth.page.models.Album.get_by_key(band_id, album_id)
        if album is None:
            raise prestans.exception.NotFound("Album")
        
        self.response.status = prestans.http.STATUS.OK
        self.response.body = prestans.ext.data.adapters.ndb.adapt_persistent_collection(
            opeth.page.models.Track.query(ancestor=album.key).fetch(),
            opeth.rest.models.Track
        )

    @prestans.provider.auth.login_required
    def post(self, band_id, album_id):
        request = self.request.parsed_body
        album = opeth.page.models.Album.get_by_key(band_id, album_id)
        track = opeth.page.models.Track(
            name=request.name, 
            parent=album.key
        )
        track.put()

        self.response.status = prestans.http.STATUS.NO_CONTENT


class RestTrackEntityHandler(Base):

    __parser_config__ = prestans.parser.Config(
        GET=prestans.parser.VerbConfig(
            response_attribute_filter_default_value=True,
            response_template=opeth.rest.models.Track()
        )
    )

    def get(self, band_id, album_id, track_id):
        track = opeth.page.models.Track.get_by_key(band_id, album_id, track_id)
        if track is None:
            raise prestans.exception.NotFound("Track")
        
        self.response.body = opeth.rest.models.Track(name=track.name)
        self.response.http_status = prestans.http.STATUS.OK

    @prestans.provider.auth.login_required
    def delete(self, band_id, album_id, track_id):
        track = opeth.page.models.Track.get_by_key(band_id, album_id, track_id)
        if track is None:
            raise prestans.exception.NotFound("Track")

        track.key.delete()
