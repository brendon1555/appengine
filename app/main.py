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

import opeth.page.handler
import opeth.rest.handler


#class MainHandler(webapp2.RequestHandler):
#    def get(self):
#        self.response.write('Hello world!')

api = prestans.rest.RequestRouter([

    (r'/api/band', opeth.rest.handler.BandCollection),
    #(r'/api/band/(\d+)', opeth.rest.handler.BandEntity),
    #(r'/api/band/(\d+)/album', opeth.rest.handler.AlbumCollection),
    #(r'/api/band/(\d+)/album/(\d+)', opeth.rest.handler.AlbumEntity)

], application_name="opeth", debug=True)

app = webapp2.WSGIApplication([
    (r'/form', opeth.page.handler.MainHandler),
    (r'/band', opeth.page.handler.BandCollection),
    (r'/band/(\d+)', opeth.page.handler.BandEntity),
    (r'/band/(\d+)/album', opeth.page.handler.AlbumCollection),
    (r'/band/(\d+)/album/(\d+)', opeth.page.handler.AlbumEntity)
], debug=True)
