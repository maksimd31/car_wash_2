from django.shortcuts import render

# Create your views here.
import requests
from django.shortcuts import render

from website2.views import authenticated_user_required
from .models import City
from .forms import CityForm


@authenticated_user_required
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=c56398aa9dd4ea5e0854302e39acf5a5'
    city = 'London'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()

        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)
    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather.html', context)


@authenticated_user_required
def weather(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=c56398aa9dd4ea5e0854302e39acf5a5'
    city = 'London'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()

        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather.html', context)
