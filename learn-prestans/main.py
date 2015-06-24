#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from google.appengine.api import users

import prestans.rest
import prestans.http
import prestans.parser
import prestans.types
import prestans.provider.auth
import prestans.ext.appengine
import prestans.ext.data.adapters.ndb

import restmodels
import pagemodels
import adapters

#webapp2
class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Get')

    def post(self):
        self.response.write('Post')


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
            response_template=prestans.types.Array(element_template=restmodels.Band())
        ),
        POST=prestans.parser.VerbConfig(
            body_template=restmodels.Band(),
            response_template=None
        )
    )

    def get(self):
        #self.logger.error("hello from get")
        bands = pagemodels.Band.query()
        
        self.response.body = prestans.ext.data.adapters.ndb.adapt_persistent_collection(
            bands,
            restmodels.Band
        )
        self.response.status = prestans.http.STATUS.OK
   
    @prestans.provider.auth.login_required
    def post(self):
        #self.logger.error("hello from post")
        request = self.request.parsed_body
        band = pagemodels.Band(
            name=request.name
        )
        band.put()
        self.response.status = prestans.http.STATUS.NO_CONTENT


class RestBandEntityHandler(Base):

    __parser_config__ = prestans.parser.Config(
        GET=prestans.parser.VerbConfig(
            response_attribute_filter_default_value=True,
            response_template=restmodels.Band()
        )
    )

    def get(self, band_id):
        band = pagemodels.Band.get_by_key(band_id)
        if band is None:
            raise prestans.exception.NotFound("Band")
        
        self.response.http_status = prestans.http.STATUS.OK
        self.response.body = restmodels.Band(name=band.name)

    @prestans.provider.auth.login_required
    def delete(self, band_id):
        #pagemodels.Band.get_by_key(band_id).key.delete()
        band = pagemodels.Band.get_by_key(band_id)
        if band is None:
            raise prestans.exception.NotFound("Band")

        pagemodels.ndb.delete_multi(pagemodels.ndb.Query(ancestor=band.key).iter(keys_only=True))


class RestAlbumCollectionHandler(Base):

    __parser_config__ = prestans.parser.Config(
        GET=prestans.parser.VerbConfig(
            response_attribute_filter_default_value=True,
            response_template=prestans.types.Array(element_template=restmodels.Album())
        ),
        POST=prestans.parser.VerbConfig(
            body_template=restmodels.Album(),
            response_template=None
        )
    )

    def get(self, band_id):
        band = pagemodels.Band.get_by_key(band_id)
        if band is None:
            raise prestans.exception.NotFound("Band")

        self.response.status = prestans.http.STATUS.OK
        self.response.body = prestans.ext.data.adapters.ndb.adapt_persistent_collection(
            pagemodels.Album.query(ancestor=band.key).fetch(),
            restmodels.Album
        )

    @prestans.provider.auth.login_required
    def post(self, band_id):
        request = self.request.parsed_body
        band = pagemodels.Band.get_by_key(band_id)
        album = pagemodels.Album(
            name=request.name, 
            parent=band.key
        )
        album.put()
        self.response.status = prestans.http.STATUS.NO_CONTENT


class RestAlbumEntityHandler(Base):

    __parser_config__ = prestans.parser.Config(
        GET=prestans.parser.VerbConfig(
            response_attribute_filter_default_value=True,
            response_template=restmodels.Album()
        )
    )

    def get(self, band_id, album_id):
        album = pagemodels.Album.get_by_key(band_id, album_id)
        if album is None:
            raise prestans.exception.NotFound("Album")
        
        self.response.http_status = prestans.http.STATUS.OK
        self.response.body = restmodels.Album(name=album.name)

    @prestans.provider.auth.login_required
    def delete(self, band_id, album_id):
        #pagemodels.Album.get_by_key(band_id, album_id).key.delete()
        album = pagemodels.Album.get_by_key(band_id, album_id)
        if album is None:
            raise prestans.exception.NotFound("Album")
        pagemodels.ndb.delete_multi(pagemodels.ndb.Query(ancestor=album.key).iter(keys_only=True))


class RestTrackCollectionHandler(Base):

    __parser_config__ = prestans.parser.Config(
        GET=prestans.parser.VerbConfig(
            response_attribute_filter_default_value=True,
            response_template=prestans.types.Array(element_template=restmodels.Track())
        ),
        POST=prestans.parser.VerbConfig(
            body_template=restmodels.Track(),
            response_template=None
        )
    )

    def get(self, band_id, album_id):
        album = pagemodels.Album.get_by_key(band_id, album_id)
        self.logger.error(album)
        if album is None:
            raise prestans.exception.NotFound("Album")
        
        self.response.status = prestans.http.STATUS.OK
        self.response.body = prestans.ext.data.adapters.ndb.adapt_persistent_collection(
            pagemodels.Track.query(ancestor=album.key).fetch(),
            restmodels.Track
        )

    @prestans.provider.auth.login_required
    def post(self, band_id, album_id):
        request = self.request.parsed_body
        album = pagemodels.Album.get_by_key(band_id, album_id)
        track = pagemodels.Track(
            name=request.name, 
            parent=album.key
        )
        track.put()

        self.response.status = prestans.http.STATUS.NO_CONTENT


class RestTrackEntityHandler(Base):

    __parser_config__ = prestans.parser.Config(
        GET=prestans.parser.VerbConfig(
            response_attribute_filter_default_value=True,
            response_template=restmodels.Track()
        )
    )

    def get(self, band_id, album_id, track_id):
        track = pagemodels.Track.get_by_key(band_id, album_id, track_id)
        if track is None:
            raise prestans.exception.NotFound("Track")
        
        self.response.body = restmodels.Track(name=track.name)
        self.response.http_status = prestans.http.STATUS.OK

    @prestans.provider.auth.login_required
    def delete(self, band_id, album_id, track_id):
        track = pagemodels.Track.get_by_key(band_id, album_id, track_id)
        if track is None:
            raise prestans.exception.NotFound("Track")

        track.key.delete()


#webapp2 router
app = webapp2.WSGIApplication([
    ('/logout', MainHandler)
], debug=True)

#prestans router
api = prestans.rest.RequestRouter(routes=[
    (r'/api/login', LoginHandler),
    (r'/api/logout', LogoutHandler),
    (r'/api/band', RestBandCollectionHandler),
    (r'/api/band/(\d+)', RestBandEntityHandler),
    (r'/api/band/(\d+)/album', RestAlbumCollectionHandler),
    (r'/api/band/(\d+)/album/(\d+)', RestAlbumEntityHandler),
    (r'/api/band/(\d+)/album/(\d+)/track', RestTrackCollectionHandler),
    (r'/api/band/(\d+)/album/(\d+)/track/(\d+)', RestTrackEntityHandler)
    ],
    application_name="learn-prestans",
    debug=True)