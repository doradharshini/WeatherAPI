from django.shortcuts import render, redirect
from requests import get, codes
from datetime import datetime
import random
from django.contrib import messages

ip = get('https://api.ipify.org').text
response = get(f'https://ipapi.co/{ip}/json/').json()
data = {
    # "city": response.get("city"),
    "region": response.get("region"),
    # "country": response.get("country_name")
}

data['region'] = "India" #Default region

api_url = 'https://api.api-ninjas.com/v1/weather?city={}'.format(data['region'])
mycityres = get(api_url, headers={'X-Api-Key': '/o/qGnffipWp3BOJ9LLl7g==blTrqJzDKNBbuZD7'})


def home(request):
    if mycityres.status_code == codes.ok:
        weather = dict(mycityres.json())

        if weather['temp'] < weather['min_temp'] or weather['temp'] >  weather['max_temp']:
            condition = "Extreme"
        elif  weather['humidity'] > 80:
            condition = "Humid"
        elif  weather['wind_speed'] > 20:
            condition = "Windy"
        elif weather['temp'] < 10:
            condition = "Cold"
        elif weather['temp'] > 30:
            condition = "Hot"
        else:
            condition = "Rainy" if weather['humidity'] > 70 else "Normal"

        time = datetime.now().hour #-> showing server time while hosting 

        return render(request, 'index.html', {"region":data['region'] , "condition":condition ,"temp":weather['temp'] ,"time":time})
    else:
        return redirect(request.META.get('HTTP_REFERER'))
    
def weather(request, city):
    api_url = 'https://api.api-ninjas.com/v1/weather?city={}'.format(city)
    cityres = get(api_url, headers={'X-Api-Key': '/o/qGnffipWp3BOJ9LLl7g==blTrqJzDKNBbuZD7'})
    if cityres.status_code == codes.ok:
        weather = dict(cityres.json())

        if weather['temp'] < weather['min_temp'] or weather['temp'] >  weather['max_temp']:
            condition = "Extreme"
        elif  weather['humidity'] > 80:
            condition = "Humid"
        elif  weather['wind_speed'] > 20:
            condition = "Windy"
        elif weather['temp'] < 10:
            condition = "Cold"
        elif weather['temp'] > 30:
            condition = "Hot"
        else:
            condition = "Rainy" if weather['humidity'] > 70 else "Normal"


        return render(request, 'weather.html', {"region":data['region'],
                                              "city":city.capitalize(),
                                              "condition":condition,
                                              "temp":weather['temp'],
                                              "humidity":weather['humidity'],
                                              "wind_speed":weather['wind_speed'],
                                              "yesterday":random.randint(weather['min_temp'], weather['max_temp']),
                                              "tomorrow":random.randint(weather['min_temp'], weather['max_temp']),
                                              "sunset":datetime.fromtimestamp(weather['sunset']).strftime("%I:%M %p"),
                                              "sunrise":datetime.fromtimestamp(weather['sunrise']).strftime("%I:%M %p")})
    else:
        return redirect(request.META.get('HTTP_REFERER'))

def city(request):
    if(request.method == "POST"):
        city = request.POST['city']
        api_url = 'https://api.api-ninjas.com/v1/weather?city={}'.format(city)
        cityres = get(api_url, headers={'X-Api-Key': '/o/qGnffipWp3BOJ9LLl7g==blTrqJzDKNBbuZD7'})
        if cityres.status_code == codes.ok:
            weather = dict(cityres.json())

            if weather['temp'] < weather['min_temp'] or weather['temp'] >  weather['max_temp']:
                condition = "Extreme"
            elif  weather['humidity'] > 80:
                condition = "Humid"
            elif  weather['wind_speed'] > 20:
                condition = "Windy"
            elif weather['temp'] < 10:
                condition = "Cold"
            elif weather['temp'] > 30:
                condition = "Hot"
            else:
                condition = "Rainy" if weather['humidity'] > 70 else "Normal"

            return render(request, 'weather.html', {"region":data['region'],
                                                "city":city.capitalize(),
                                                "condition":condition,
                                                "temp":weather['temp'],
                                                "humidity":weather['humidity'],
                                                "wind_speed":weather['wind_speed'],
                                                "yesterday":random.randint(weather['min_temp'], weather['max_temp']),
                                                "tomorrow":random.randint(weather['min_temp'], weather['max_temp']),
                                                "sunset":datetime.fromtimestamp(weather['sunset']).strftime("%I:%M %p"),
                                                "sunrise":datetime.fromtimestamp(weather['sunrise']).strftime("%I:%M %p")})
        else:
            messages.warning(request, "No city found!" )
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.warning(request, "No city found!" )
        return redirect(request.META.get('HTTP_REFERER'))