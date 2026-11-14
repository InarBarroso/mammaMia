from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Pizza, TipoMasa

# Create your views here.



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

def allmasas(request):
    masas = TipoMasa.objects.all()
    context = {
        'masas': masas
    }
    return render(request, "allMasas.html", context)

def filtrarmasa(request, idMasa):
    masa = get_object_or_404(TipoMasa, pk=idMasa)
    # pizzas que tienen esta masa
    pizzas = Pizza.objects.filter(tipo=masa)
    context = {
        'masa': masa,
        'pizzas': pizzas
    }
    return render(request, "detalle_masa.html", context)

def login_view(request):
    # página de inicio de sesión --> /login
    # paso 1: solo muestra la página; el formulario y el acceso llegan en los siguientes pasos
    return render(request, 'login.html')

def addpizza(request):
    masas = TipoMasa.objects.all()
    context = {
        'masas': masas
    }
    return render(request, "addPizzaAdmin.html", context)