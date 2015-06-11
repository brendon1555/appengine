from google.appengine.ext import ndb

class Comment(ndb.Model):
    content = ndb.StringProperty()