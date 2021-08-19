import requests
from datetime import date
from django.shortcuts import render
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid='
    cities = City.objects.all()
    ct=[]
    for i in cities:
        ct.append(i.name.upper())
    print(ct)    
    
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.data['name'].upper() not in ct:
            form.save()
        

    form = CityForm()
    today=date.today()
    
    weather_data = []
    names=[]
    
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
            
            weather_data.append(data)
        else:
            continue
    
    final={'weather_data':weather_data,'form':form,'date':today}

    return render(request, 'index.html',final)

