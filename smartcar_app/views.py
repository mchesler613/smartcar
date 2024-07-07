from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from smartcar import SmartcarException

import smartcar

# Ensure SETUP is completed, then instantiate an AuthClient
client = smartcar.AuthClient(mode="test")

# scope of permissions
scope = ["read_vehicle_info"]


# Create your views here.
def authorize(request: HttpRequest):
    """
    This view logins the user and authorizes the app to retrieve
    scoped vehicle data from SmartConnect
    """
    auth_url = client.get_auth_url(scope)
    print('auth_url', auth_url)
    response = redirect(auth_url)
    return response


def exchange_code(request: HttpRequest):
    """
    To work, this route must be in your Smartcar developer dashboard
    as a Redirect URI.

    i.e. "http://localhost:8000/exchange/"
    """
    code = request.GET.get("code")

    # save access_token in request's session
    request.session['access_token'] = client.exchange_code(code).access_token

    # redirect the response the /vehicles/ endpoint
    response = redirect("/vehicles/")
    return response


def get_vehicles(request: HttpRequest):
    """
    This function returns a list of vehicle data from the authorized scope
    """
    # retrieve the access token from the request session
    access_token = request.session['access_token']

    # receive a list of vehicle data
    # `Vehicles` NamedTuple, which has an attribute of 'vehicles' and 'meta'
    result = smartcar.get_vehicles(access_token)
    import pp
    pp(result)

    response_list = []

    for vehicle_id in result.vehicles:
        # instantiate a vehicle based on its id
        vehicle = smartcar.Vehicle(vehicle_id, access_token)
        pp(vehicle.__dict__)

        # use the attributes() method to call to Smartcar API and
        # get information about the vehicle.

        # These vehicle methods return NamedTuples with attributes
        attributes = vehicle.attributes()
        response_list.append(
            {
                "id": vehicle_id,
                "make": attributes.make,
                "model": attributes.model,
                "year": attributes.year
            }
        )
    response = JsonResponse(response_list, safe=False)
    return response


def get_a_vehicle(request, id):
    """
    This method returns a single vehicle data based on its id
    in the path parameter
    """
    vehicle_id = id

    # retrieve the access token from the session
    access_token = request.session['access_token']

    # receive a `Vehicles` NamedTuple, which has an attribute of
    # 'vehicles' and 'meta'
    result = smartcar.get_vehicles(access_token)

    # match the id with result.vehicles
    if vehicle_id not in result.vehicles:
        raise SmartcarException(
            message=f"invalid vehicle id {vehicle_id}"
        )

    # instantiate the first vehicle in the vehicle id list
    vehicle = smartcar.Vehicle(vehicle_id, access_token)

    # use the attributes() method to call to Smartcar API and get
    # information about the vehicle.
    # These vehicle methods return NamedTuples with attributes
    attributes = vehicle.attributes()

    response = JsonResponse(
        {
            "id": vehicle_id,
            "make": attributes.make,
            "model": attributes.model,
            "year": attributes.year
        }
    )
    return response
