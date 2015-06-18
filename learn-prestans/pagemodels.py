from google.appengine.ext import ndb

import prestans.ext.data.adapters
import prestans.ext.data.adapters.ndb

class Band(ndb.Model):
    name = ndb.StringProperty()