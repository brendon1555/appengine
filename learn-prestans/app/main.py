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
import opeth.rest.handlers
import opeth.page.handlers
import prestans.rest

#webapp2 router
app = webapp2.WSGIApplication([
    ('/', opeth.page.handlers.MainHandler)
], debug=True)

#prestans router
api = prestans.rest.RequestRouter(routes=[
    (r'/api/login', opeth.rest.handlers.LoginHandler),
    (r'/api/logout', opeth.rest.handlers.LogoutHandler),
    (r'/api/band', opeth.rest.handlers.RestBandCollectionHandler),
    (r'/api/band/(\d+)', opeth.rest.handlers.RestBandEntityHandler),
    (r'/api/band/(\d+)/album', opeth.rest.handlers.RestAlbumCollectionHandler),
    (r'/api/band/(\d+)/album/(\d+)', opeth.rest.handlers.RestAlbumEntityHandler),
    (r'/api/band/(\d+)/album/(\d+)/track', opeth.rest.handlers.RestTrackCollectionHandler),
    (r'/api/band/(\d+)/album/(\d+)/track/(\d+)', opeth.rest.handlers.RestTrackEntityHandler)
    ],
    application_name="learn-prestans",
    debug=True)