import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=091b860ff3d1aa8a0e68ccb9b548f25b'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()
    weather_data = []
    names=[]
    print(cities)
    for i in cities:
        if i.name.upper() not in names:
            names.append(i.name.upper())
            r=requests.get(url.format(i.name)).json()
            if len(r)<=2:
                pass
            else:
                data={
                    'city' : i.name.upper(),
                    'temperature' : r['main']['temp'],
                    'description' : r['weather'][0]['description'],
                    'icon' : r['weather'][0]['icon']
                }
            print(data)
            weather_data.append(data)
        else:
            continue
    print(names)
    final={'weather_data':weather_data,'form':form}

    return render(request, 'index.html',final)
