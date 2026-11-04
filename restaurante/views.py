from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the restaurante index.")


def home(request):
    return render(request, "cover.html")
    context = {
        'pizzas' : pizzas

def filtrarpizza(request, idPizza):
    //implementar la vista para filtrar pizza por id


