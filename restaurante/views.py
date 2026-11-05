from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Pizza

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the restaurante index.")


def home(request):
    pizzas = Pizza.objects.order_by('-num_ventas')[:3]
    context = {
        'pizzas' : pizzas
    }
    return render(request, "cover.html", context)

def filtrarpizza(request, idPizza):
    # detalle de una pizza --> /pizza/<idPizza>
    # busca la pizza por su id; si no existe, lanza Http404 automáticamente
    pizza = get_object_or_404(Pizza, pk=idPizza)

    # los ingredientes se guardan como texto: "Tomate, Mozzarella, Albahaca"
    # lo separamos por las comas para poder mostrarlos como lista en el template
    ingredientes = [i.strip() for i in pizza.ingredientes.split(',') if i.strip()]

    contexto = {
        'pizza': pizza,
        'ingredientes': ingredientes,
    }
    return render(request, 'detalle_pizza.html', contexto)

def allpizzas(request):
    pizzas = Pizza.objects.all()
    context = {
        'pizzas': pizzas
    }
    return render(request, "allPizza.html", context)


