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
import prestans.rest
import prestans.http
import prestans.parser
import prestans.types
import prestans.provider.auth

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
class RestBandCollectionHandler(prestans.rest.RequestHandler):

    __parser_config__ = prestans.parser.Config(
        GET=prestans.parser.VerbConfig(
            response_attribute_filter_default_value=True,
            response_template=prestans.types.Array(element_template=restmodels.Band())
        ),
        POST=prestans.parser.VerbConfig(
            body_template=restmodels.Band(),
            response_attribute_filter_default_value=True,
            response_template=None
        )
    )

    @prestans.provider.auth.login_required
    def get(self):
        #self.logger.error("hello from get")
        bands = pagemodels.Band.query()
        if bands == []:
            raise prestans.exception.NotFound("No Bands were found")
        else:
            self.response.body = prestans.ext.data.adapters.ndb.adapt_persistent_collection(
                bands,
                restmodels.Band
            )
            self.response.status = prestans.http.STATUS.OK
        
    def post(self):
        #self.logger.error("hello from post")
        request = self.request.parsed_body
        pagemodels.Band(name=request.name).put()
        self.response.status = prestans.http.STATUS.NO_CONTENT


class RestBandEntityHandler(prestans.rest.RequestHandler):

    __parser_config__ = prestans.parser.Config(
        GET=prestans.parser.VerbConfig(
            response_attribute_filter_default_value=True,
            response_template=restmodels.Band()
        )
    )

    def get(self, band_id):
        band_key = pagemodels.Band.get_by_key(band_id).get()
        if band_key is None:
            raise prestans.exception.NotFound("The band was not found")
        else:
            self.response.http_status = prestans.http.STATUS.OK
            self.response.body = restmodels.Band(name=band_key.name)

    def delete(self, band_id):
        pagemodels.Band.get_by_key(band_id).delete()


class RestAlbumCollectionHandler(prestans.rest.RequestHandler):

    __parser_config__ = prestans.parser.Config(
        GET=prestans.parser.VerbConfig(
            response_attribute_filter_default_value=True,
            response_template=prestans.types.Array(element_template=restmodels.Album())
        ),
        POST=prestans.parser.VerbConfig(
            body_template=restmodels.Album(),
            response_attribute_filter_default_value=True,
            response_template=restmodels.Album()
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


    def post(self, band_id):
        request = self.request.parsed_body

        album = pagemodels.Album.make_key(band_id, request)
        album.put()
        self.response.status = prestans.http.STATUS.NO_CONTENT


class RestAlbumEntityHandler(prestans.rest.RequestHandler):

    __parser_config__ = prestans.parser.Config(
        GET=prestans.parser.VerbConfig(
            response_attribute_filter_default_value=True,
            response_template=restmodels.Album()
        )
    )

    def get(self, band_id, album_id):
        album_key = pagemodels.Album.get_by_key(band_id, album_id).get()
        if album_key is None:
            raise prestans.exception.NotFound("The album was not found")
        else:
            self.response.http_status = prestans.http.STATUS.OK
            self.response.body = restmodels.Album(name=album_key.name)

    def delete(self, band_id, album_id):
        pagemodels.Album.get_by_key(band_id, album_id).delete()


class RestTrackCollectionHandler(prestans.rest.RequestHandler):

    __parser_config__ = prestans.parser.Config(
        GET=prestans.parser.VerbConfig(
            response_attribute_filter_default_value=True,
            response_template=prestans.types.Array(element_template=restmodels.Track())
        ),
        POST=prestans.parser.VerbConfig(
            body_template=restmodels.Track(),
            response_attribute_filter_default_value=True,
            response_template=restmodels.Track()
        )
    )

    def get(self, band_id, album_id):
        album_key = pagemodels.Album.get_by_key(band_id, album_id)
        tracks = pagemodels.Track.query(ancestor=album_key).fetch()
        if tracks == []:
            raise prestans.exception.NotFound("No Tracks were found")
        else:
            self.response.body = prestans.ext.data.adapters.ndb.adapt_persistent_collection(
                tracks,
                restmodels.Track
            )
            self.response.status = prestans.http.STATUS.OK

    def post(self, band_id, album_id):
        request = self.request.parsed_body

        track = pagemodels.Track.make_key(band_id, album_id, request)
        track.put()

        self.response.status = prestans.http.STATUS.NO_CONTENT


class RestTrackEntityHandler(prestans.rest.RequestHandler):

    __parser_config__ = prestans.parser.Config(
        GET=prestans.parser.VerbConfig(
            response_attribute_filter_default_value=True,
            response_template=restmodels.Track()
        )
    )

    def get(self, band_id, album_id, track_id):
        track_key = pagemodels.Track.get_by_key(band_id, album_id, track_id).get()
        if track_key is None:
            raise prestans.exception.NotFound("The track was not found")
        else:
            self.response.body = restmodels.Track(name=track_key.name)
            self.response.http_status = prestans.http.STATUS.OK

    def delete(self, band_id, album_id, track_id):
        pagemodels.Track.get_by_key(band_id, album_id, track_id).delete()

#webapp2 router
app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)

#prestans router
api = prestans.rest.RequestRouter(routes=[
    (r'/api/band', RestBandCollectionHandler),
    (r'/api/band/(\d+)', RestBandEntityHandler),
    (r'/api/band/(\d+)/album', RestAlbumCollectionHandler),
    (r'/api/band/(\d+)/album/(\d+)', RestAlbumEntityHandler),
    (r'/api/band/(\d+)/album/(\d+)/track', RestTrackCollectionHandler),
    (r'/api/band/(\d+)/album/(\d+)/track/(\d+)', RestTrackEntityHandler)
    ],
    application_name="learn-prestans",
    debug=True)