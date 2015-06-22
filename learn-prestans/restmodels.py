import prestans.types

class Base(prestans.types.Model):
    id = prestans.types.String(required=False)

class Track(Base):
    name = prestans.types.String(required=True)

class Album(Base):
    name = prestans.types.String(required=True)

class Band(Base):
    name = prestans.types.String(required=True)
    #albums = prestans.types.Array(element_template=Album(), required=False)