from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the restaurante index.")


def home(request):
    return render(request, "cover.html")
    pizzas = pizza.objects.all() # aqui solo cogeremos las 3 mas vendidas
    context = {
        'pizzas' : pizzas
    }

def filtrarpizza(request, idPizza, name="filtrarpizza"):
    #implementar la vista para filtrar pizza por id


