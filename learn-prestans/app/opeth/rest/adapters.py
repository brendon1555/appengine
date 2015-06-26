import prestans
import opeth.page.models
import opeth.rest.models


# Register the persistent model to adapt to the Band rest model, also
# ensure that Album is registered for the children models to adapt
prestans.ext.data.adapters.registry.register_adapter(
    prestans.ext.data.adapters.ndb.ModelAdapter(
        rest_model_class=opeth.rest.models.Band,
        persistent_model_class=opeth.page.models.Band
    )
)

prestans.ext.data.adapters.registry.register_adapter(
    prestans.ext.data.adapters.ndb.ModelAdapter(
        rest_model_class=opeth.rest.models.Album,
        persistent_model_class=opeth.page.models.Album
    )
)

prestans.ext.data.adapters.registry.register_adapter(
    prestans.ext.data.adapters.ndb.ModelAdapter(
        rest_model_class=opeth.rest.models.Track,
        persistent_model_class=opeth.page.models.Track
    )
)