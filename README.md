# Django with Smartcar API Integration

If you have a modern vehicle with [telemetry](https://en.wikipedia.org/wiki/Telemetry) installed and remote access via a mobile app, such as Toyota Connected Services, and other similar apps, you can use the [Smartcar](http://smartcar.com) [API](https://github.com/smartcar/python-sdk/tree/master) to retrieve data
for your vehicle and [other supported brands](https://smartcar.com/product/compatible-vehicles).

I was asked to play around with the Smartcar API and I obliged. After a brief exploration, I found
that the Smartcar tutorial comes with Python SDK samples that work with the [Flask Web Framework](https://flask.palletsprojects.com/en/3.0.x/).  Having been a Djangonaut for the past several years, I can't help but create a miniature Django WIP (Work-in-progress) version for this.

# GOALS
At the end of this article, you will be able to:
- run a local [Django](http://djangoproject.com) service to query a small sampling of the Smartcar APIs to return vehicle data with the [OAuth2](https://testdriven.io/blog/oauth-python/) web protocol.

# Dev Environment Part 1
For this tutorial, I set up my development environment with [Poetry](https://python-poetry.org/docs/) and [Pyenv](https://github.com/pyenv).
To begin:

- git clone this repo
- activate pyenv for python 3.12
```
pyenv shell 3.12
```
- configure poetry to use pyenv
```
poetry env use 3.12
```
- activate poetry's virtual environment
```
source $(poetry env info --path)/bin/activate
```
- run `poetry install`

# Set up credentials at Smartcar
- Create a [developer account](https://dashboard.smartcar.com/signup) at Smartcar
- Login to your developer account and copy the values for these 2 important credentials
   - `SMARTCAR_CLIENT_ID`
   - `SMARTCAR_CLIENT_SECRET`
to be exported later to your development environemnt.
- Set the value of this credential 
   - `SMARTCAR_REDIRECT_URI`
   to point to `http://localhost:8000/exchange/`

# Dev Environment Part 2
- export the 3 smartcar credentials to your local environment
- don't forget to setup your `DJANGO_SETTINGS_MODULE` as well to `django_smartcar.settings`
- migrate your Django migration files
```
./manage.py migrate
```
- run your Django server locally
```
./manage.py runserver
```
- open up a browser and access your Django service at `http://localhost:8000`. This url will redirect you to this page to connect to your vehicle's connected service app.

![login](https://i.postimg.cc/L4xb3HvF/2024-07-07-15-53-39.jpg)
- Click `Continue` and login to your vehicle's remote connect app
- You will be presented with a view like this (if you have a Toyota)
![authorize](https://i.postimg.cc/W3qrxwgv/2024-07-07-15-57-20.jpg)
- Click on the `Toyota` to proceed to this page
![allow](https://i.postimg.cc/gjjgrTw6/2024-07-07-16-02-35.jpg)
- Since the data is fake, you might as well click `Allow` to proceed
- You are redirected to this Django endpoint that is created for this app, `/localhost:8000/vehicles/` which list the vehicles that you alllowed for access
![vehicles list](https://i.postimg.cc/MGbDKSGG/2024-07-07-16-08-39.jpg)
- If you are interested in only one vechile at a time, you can pass the `id` to this endpoint that I created for this app, `/localhost:8000/vehicles/<str:id>/`
![one vehicle](https://i.postimg.cc/D0qjsXvq/2024-07-07-16-11-56.jpg)

# Summary
There are 4 endpoints created for this Django app that integrates with the Smartcar API.
- `/authorize/`, which is redirected from `http://localhost:8000/` to retrieve an authorization url
- `/exchange/`,  is the redirect_url that is waiting to receive a `code` from the authorization url. This code is exchanged for an `access code` to be passed to subsequent queries for vehicle data
- `/vehicles/`, is the list endpoint that returns a list of allowed vehicles for viewing using the `access code` 
- `/vehicles/<str:id>`, is a single retrieve endpoint for vehicle data based on its id and using the `access code`

Last but not least, you can extend this app to include a more comprehensive listing of Smartcar API endpoints and have fun. Happy Django! 
