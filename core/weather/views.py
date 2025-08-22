from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

# Create your views here.


@method_decorator(cache_page(60 * 20), name="dispatch")
class WeatherView(APIView):
    def get(self, request, city, *args, **kwargs):
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"q={city}&appid=YOUR_API_KEY"
        )
        return Response(response.json())
