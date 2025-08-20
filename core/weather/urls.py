from django.urls import path
from .views import WeatherView

urlpatterns = [
    path("<str:city>/", WeatherView.as_view(), name="weather"),
]
