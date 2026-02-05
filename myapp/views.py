from django.shortcuts import render,redirect
from .forms import CityForm
from .models import City
import requests
from django.contrib import messages

# Create your views here.def home(request):
def home(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=b2a12beda58827d40b6442b2f8c81f87'

    data = []   # 🔥 important – outside if/else

    if request.method == "POST":
        form = CityForm(request.POST)

        if form.is_valid():
            NCity = form.cleaned_data['name']
            CCity = City.objects.filter(name=NCity).count()

            if CCity == 0:
                res = requests.get(url.format(NCity)).json()

                if res.get('cod') == 200:
                    form.save()
                    messages.success(request, f"{NCity} Added Successfully...!!!")
                else:
                    messages.error(request, "City Does Not Exist...!!!")
            else:
                messages.error(request, "City Already Exists...!!!")

    else:
        form = CityForm()

    # 🔥 COMMON PART – GET & POST both
    cities = City.objects.all()
    for city in cities:
        res = requests.get(url.format(city.name)).json()

        if res.get('cod') == 200:
            city_weather = {
                'city': city.name,
                'temperature': res['main']['temp'],
                'description': res['weather'][0]['description'],
                'country': res['sys']['country'],
                'icon': res['weather'][0]['icon'],
            }
            data.append(city_weather)

    context = {
        'data': data,
        'form': form
    }
    return render(request, 'weather.html', context)



def delete_city(request,CName):
    City.objects.filter(name=CName).delete()
    messages.success(request," " + CName + " Removed Successfully...!!")
    return redirect('home')