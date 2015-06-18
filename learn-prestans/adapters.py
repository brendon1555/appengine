import prestans
import pagemodels
import restmodels


# Register the persistent model to adapt to the Band rest model, also
# ensure that Album is registered for the children models to adapt
prestans.ext.data.adapters.registry.register_adapter(
    prestans.ext.data.adapters.ndb.ModelAdapter(
        rest_model_class=restmodels.Band,
        persistent_model_class=pagemodels.Band
    )
)