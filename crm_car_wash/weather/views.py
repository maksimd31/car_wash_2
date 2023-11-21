from django.shortcuts import render

# Create your views here.
import requests
from django.shortcuts import render

from website2.views import authenticated_user_required
from .models import City
from .forms import CityForm

# @authenticated_user_required
# def index(request):
#     url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=c56398aa9dd4ea5e0854302e39acf5a5'
#     city = 'London'
#
#     if request.method == 'POST':
#         form = CityForm(request.POST)
#         form.save()
#
#     form = CityForm()
#
#     cities = City.objects.all()
#
#     weather_data = []
#
#     for city in cities:
#         r = requests.get(url.format(city)).json()
#
#         city_weather = {
#             'city': city.name,
#             'temperature': r['main']['temp'],
#             'description': r['weather'][0]['description'],
#             'icon': r['weather'][0]['icon'],
#         }
#
#         weather_data.append(city_weather)
#     context = {'weather_data': weather_data, 'form': form}
#     return render(request, 'weather.html', context)
#
# @authenticated_user_required
# def index(request):
#     url = '<http://api.openweathermap.org/data/2.5/weather?q=Moscow&units=metric&appid=ad71d819492af038206fc7075fea00fa'
#
#     cities = ['Moscow']
#
#     weather_data = []
#
#     for city in cities:
#         r = requests.get(url).json()
#
#         city_weather = {
#             'city': city,
#             'temperature': r['main']['temp'],
#             'description': r['weather'][0]['description'],
#             'icon': r['weather'][0]['icon'],
#         }
#
#         weather_data.append(city_weather)
#     context = {'weather_data': weather_data}
#     return render(request, 'weather.html', context)
#
#
# @authenticated_user_required
# def weather(request):
#     url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=c56398aa9dd4ea5e0854302e39acf5a5'
#     city = 'London'
#
#     if request.method == 'POST':
#         form = CityForm(request.POST)
#         form.save()
#
#     form = CityForm()
#
#     cities = City.objects.all()
#
#     weather_data = []
#
#     for city in cities:
#         r = requests.get(url.format(city)).json()
#
#         city_weather = {
#             'city': city.name,
#             'temperature': r['main']['temp'],
#             'description': r['weather'][0]['description'],
#             'icon': r['weather'][0]['icon'],
#         }
#
#         weather_data.append(city_weather)
#
#     context = {'weather_data': weather_data, 'form': form}
#     return render(request, 'weather.html', context)


from django.shortcuts import render
# import json to load json data to python dictionary
import json
# urllib.request to make a request to api
import urllib.request


def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        ''' api key might be expired use your own api_key 
            place api_key in place of appid ="your_api_key_here " '''

        # source contain JSON data from API

        source = urllib.request.urlopen(
            'http://api.openweathermap.org/data/2.5/weather?q ='
            + city + '&appid = ad71d819492af038206fc7075fea00fa').read()

        # converting JSON data to a dictionary
        list_of_data = json.loads(source)

        # data for variable list_of_data
        data = {
            "country_code": str(list_of_data['sys']['country']),
            "coordinate": str(list_of_data['coord']['lon']) + ' '
                          + str(list_of_data['coord']['lat']),
            "temp": str(list_of_data['main']['temp']) + 'k',
            "pressure": str(list_of_data['main']['pressure']),
            "humidity": str(list_of_data['main']['humidity']),
        }
        print(data)
    else:
        data = {}
    return render(request, "index.html", data)
