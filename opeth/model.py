from google.appengine.ext import ndb

class Comment(ndb.Model):
    content = ndb.StringProperty()
    date_added = ndb.DateTimeProperty(auto_now_add=True)