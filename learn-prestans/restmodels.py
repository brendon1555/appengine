import prestans.types

class Band(prestans.types.Model):
    name = prestans.types.String(required=True)