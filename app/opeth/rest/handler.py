import prestans.rest
import prestans.parser

import opeth.rest.model
import opeth.model

band_create_filter = prestans.parser.AttributeFilter.from_model(opeth.rest.model.Band())

class BandCollection(prestans.rest.RequestHandler):
    __parser_config__ = prestans.parser.Config(
        GET=prestans.parser.VerbConfig(
            response_template=prestans.types.Array(element_template=opeth.rest.model.Band())
        ),
        POST=prestans.parser.VerbConfig(
            body_template=opeth.rest.model.Band(),
            response_template=opeth.rest.model.Band()
        )
    )

    def get(self):
        bands = opeth.model.Band.query()

        self.response.http_status = prestans.http.STATUS_OK
        self.response.body = prestans.ext.data.adapters.ndb.adapt_persistent_collection(
            band, 
            opeth.rest.model.Band, 
            self.response.attribute_filter)

    def post(self):
        band_rest_model = self.request.parsed_body

        band.name = band_rest_model.name