from django.shortcuts import render
from datetime import datetime
import requests
import locale

base_url_city='https://eu1.locationiq.com/v1/search.php?key=a1779b7817b3b2&q=[location]&format=json'
base_url_weather='https://api.darksky.net/forecast/[key]/[latitude],[longitude]'



# Create your views here.

def index(request):

    if request.method =="POST":
        
        city = request.POST.get("city")

        city_url = 'https://eu1.locationiq.com/v1/search.php?key=a1779b7817b3b2&q='+ city +'&format=json'

        response_city = requests.get(city_url)

        response_cityjson = response_city.json()

        lat = response_cityjson[0]['lat']

        lon = response_cityjson[0]['lon']

        weather_url= 'https://api.darksky.net/forecast/c6c6c99fc75c7a4206c51ac8bbd866c6/'+ lat + ',' + lon

        response_weather = requests.get(weather_url)

        response_weatherjson = response_weather.json()

        now_temperature = response_weatherjson['currently']['temperature']

        # T(°C) = (68°F - 32) × 5/9 = 20 °C

        Cnow_temperature=(now_temperature-32)*(5/9)

        Cnow_temperature=round(Cnow_temperature) #Alta veya üste yuvarlıyor. # Şuanki sıcaklık 

        now_icon=response_weatherjson['currently']['icon']


        # print(response_weatherjson['daily']['data'][0]['time'])

        days=list()        #Hafta'nın  hava durumu bilgilerini tutmak için

        for i in  response_weatherjson['daily']['data']: 
            
            icon=i['icon']
            time=i['time']
            temparatureMin=i["temperatureMin"]
            CtemparatureMin=(temparatureMin-32)*(5/9)    #F--->C
            CtemparatureMin=round(CtemparatureMin)

            temparatureMax=i["temperatureMax"]
            CtemparatureMax=(temparatureMax-32)*(5/9)
            CtemparatureMax=round(CtemparatureMax)




                                              
            time_day= datetime.strftime(datetime.fromtimestamp(time),'%A')
            

            days.append([time_day,icon,CtemparatureMin,CtemparatureMax])
        
        context = {
            'city':city,
            'Cnow':Cnow_temperature,
            'now_icon':now_icon,
            'days':days
        }

        return render(request,'weather.html',context)

    else:

        return render(request,'weather.html')
