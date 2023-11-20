from django.core.management import BaseCommand
from pyowm import OWM


class Command(BaseCommand):
    """Команда для заполнения таблицы Client случайными данными."""

    help = 'Прогноз погоды'

    def weather_forecast(city):
        """Получает прогноз погоды для указанного города"""
        owm = OWM('ad71d819492af038206fc7075fea00fa')
        mgr = owm.weather_manager()

        observation = mgr.weather_at_place(city)
        w = observation.weather

        detailed_status = w.detailed_status
        wind = w.wind()
        humidity = w.humidity
        temperature = w.temperature('celsius')['temp']
        rain = w.rain
        heat_index = w.heat_index
        clouds = w.clouds

        forecast = {
            'detailed_status': detailed_status,
            'wind': wind,
            'humidity': humidity,
            'temperature': temperature,
            'rain': rain,
            'heat_index': heat_index,
            'clouds': clouds
        }

        return forecast

    city = "Москва"
    weather = weather_forecast(city)