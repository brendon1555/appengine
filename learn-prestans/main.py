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
class RestCollectionHandler(prestans.rest.RequestHandler):

    __parser_config__ = prestans.parser.Config(
        GET=prestans.parser.VerbConfig(
            response_attribute_filter_default_value=True,
            response_template=prestans.types.Array(element_template=restmodels.Band())
        ),
        POST=prestans.parser.VerbConfig(
            body_template=restmodels.Band(),
            response_attribute_filter_default_value=True,
            response_template=restmodels.Band()
        )
    )

    def get(self):
        #self.logger.error("hello from get")
        self.response.status = prestans.http.STATUS.OK
        #bands = prestans.types.Array(element_template=restmodels.Band())
        #bands.append(restmodels.Band(name="Opeth"))
        #bands.append(restmodels.Band(name="Dark Funeral"))

        bands = pagemodels.Band.query()

        self.response.body = prestans.ext.data.adapters.ndb.adapt_persistent_collection(
            bands,
            restmodels.Band()
        )
        
    def post(self):
        #self.logger.error("hello from post")
        request = self.request.parsed_body
        pagemodels.Band(name=request.name).put()
        self.response.status = prestans.http.STATUS.NO_CONTENT
        self.response.body = request


class RestEntityHandler(prestans.rest.RequestHandler):

    __parser_config__ = prestans.parser.Config(
        GET=prestans.parser.VerbConfig(
            response_attribute_filter_default_value=True,
            response_template=restmodels.Band()
        )
    )

    def get(self, band_id):
        band_key = pagemodels.ndb.Key("Band", int(band_id)).get()
        self.response.http_status = prestans.http.STATUS.OK
        self.response.body = restmodels.Band(name=band_key.name)

    def delete(self, band_id):
        pagemodels.ndb.Key("Band", int(band_id)).delete()

#webapp2 router
app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)

#prestans router
api = prestans.rest.RequestRouter(routes=[
    ('/api/band', RestCollectionHandler),
    (r'/api/band/(\d+)', RestEntityHandler)
    ],
    application_name="learn-prestans",
    debug=True)