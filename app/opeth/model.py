from google.appengine.ext import ndb

class Band(ndb.Model):
    name = ndb.StringProperty()
    date_added = ndb.DateTimeProperty(auto_now_add=True)

class Album(ndb.Model):
    name = ndb.StringProperty()
    date_added = ndb.DateTimeProperty(auto_now_add=True)

    band = ndb.StructuredProperty(Band)