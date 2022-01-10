from firebase_admin import firestore, initialize_app
initialize_app()
db = firestore.client()

import configuration
app = configuration.init()

from resources.energy_data import EnergyData, ReferenceZones
from resources.testing import HardSleep, SoftSleep

configuration.api.add_resource(EnergyData, '/energy_data')
configuration.api.add_resource(ReferenceZones, '/ref_zones')

configuration.api.add_resource(HardSleep, '/testing/hard_sleep/<sleep_id>')
configuration.api.add_resource(SoftSleep, '/testing/soft_sleep/<sleep_id>')


# Comply with Cloud Functions code structure for entry point
def run(request):
    # Create a new app context for the internal app
    internal_ctx = app.test_request_context(path=request.full_path,
                                            method=request.method)

    # Copy main request data from original request
    # According to your context, parts can be missing. Adapt here!
    internal_ctx.request.data = request.data
    internal_ctx.request.headers = request.headers

    # Activate the context
    internal_ctx.push()
    # Dispatch the request to the internal app and get the result
    return_value = app.full_dispatch_request()
    # Offload the context
    internal_ctx.pop()

    # Return the result of the internal app routing and processing
    return return_value
