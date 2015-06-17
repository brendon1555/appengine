import prestans.types

class Band(prestans.types.Model):
    name = prestans.types.String(required=True)

    date_added = prestans.types.DateTime(required=True)

class Album(prestans.types.Model):
    name = prestans.types.String(required=True)

    date_added = prestans.types.DateTime(required=True)

