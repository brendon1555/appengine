import prestans.rest
import prestans.parser

import opeth.rest.model
import opeth.model


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

        self.response.status = prestans.http.STATUS.OK
        self.response.body = prestans.ext.data.adapters.ndb.adapt_persistent_collection(
            band, 
            opeth.rest.model.Band
        )

    def post(self):
        band_rest_model = self.request.parsed_body

        band.name = band_rest_model.name