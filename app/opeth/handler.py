import cgi
import webapp2
import json
from webapp2_extras import jinja2

import opeth.model


class Base(webapp2.RequestHandler):
        #: Ensure we return a webapp2 singleton for caching
    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    #: Wrapper to reneder jinja2 template, handles exception
    def render_template(self, template_name, template_values={}):
        template_values['IS_DEBUG'] = self.app.debug
        template_file_name = "%s.html" % template_name
        self.response.out.write(self.jinja2.render_template(template_file_name, **template_values))


class MainHandler(Base):

    def get(self):
        self.render_template("form")

    def post(self):
        comment_store = opeth.model.Band(name=self.request.POST['band'])
        comment_store.put()

        ctx = opeth.model.ndb.get_context()
        ctx.clear_cache()

        comments = opeth.model.Band.query().order(opeth.model.Band.date_added)

        template_values = {'bands': bands}
        self.render_template("output", template_values)

#------------------------------#
#----Working with XHR below----#
#------------------------------#


class BandCollection(Base):

    #get a list of bands from the datastore
    def get(self):
        bands = opeth.model.Band.query().order(opeth.model.Band.date_added)

        template_values = {'bands': bands}
        self.render_template("band", template_values)

    #add a band to the datastore
    def post(self):
        json_band = json.loads(self.request.body)

        band_store = opeth.model.Band(name=json_band["band"])
        band_key = band_store.put()

        band_id = band_key.id()

        ctx = opeth.model.ndb.get_context()
        ctx.clear_cache()

        self.response.write(band_id)

class BandEntity(Base):

    #write band name to entity url
    def get(self, band_id):
        band = opeth.model.ndb.Key("Band", int(band_id)).get()

        self.response.write(band.name)

    #delete a band from the datastore
    def delete(self, band_id):
        opeth.model.ndb.Key("Band", int(band_id)).delete()
        self.response.status = "204 No Content"

class AlbumCollection(Base):

    #get a list of albums for the current band from the datastore
    def get(self, band_id):
        band = opeth.model.ndb.Key("Band", int(band_id)).get()
        albums = opeth.model.Album.query(opeth.model.Album.band.name == band.name).order(opeth.model.Album.date_added)

        template_values = {'albums': albums, 'band': band}
        self.render_template("album", template_values)


    #add an album to the datastore
    def post(self, band_id):
        json_album = json.loads(self.request.body)

        album_store = opeth.model.Album()
        album_store.name = json_album["album"]
        album_store.band = opeth.model.Band(name=json_album["band"])
        album_key = album_store.put()

        album_id = album_key.id()

        self.response.write(album_id)


class AlbumEntity(Base):

    #send album name to entity url
    def get(self, album_id):
        album = opeth.model.ndb.Key("Album", int(album_id)).get()
        self.response.write(Album.name)

    #delete an album from the datastore
    def delete(self, band_id, album_id):
        opeth.model.ndb.Key("Album", int(album_id)).delete()
        self.response.status = "204 No Content"



app = webapp2.WSGIApplication([
    (r'/form', MainHandler),
    (r'/band', BandCollection),
    (r'/band/(\d+)', BandEntity),
    (r'/band/(\d+)/album', AlbumCollection),
    (r'/band/(\d+)/album/(\d+)', AlbumEntity)
], debug=True)