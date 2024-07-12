from django.urls import path
from smartcar_app import views
app_name = 'smartcar_app'

urlpatterns = [
    path('', views.authorize, name='home'),
    path("authorize/", views.authorize, name='authorize'),
    path("exchange/", views.exchange_code, name='exchange'),
    path("vehicles/", views.get_vehicles, name='vehicle-list'),
    path("vehicles/<str:id>/", views.get_a_vehicle, name='vehicle-detail'),
]
