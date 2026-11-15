from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Pizza, TipoMasa, Ingrediente

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

    ingredientes = pizza.ingredientes.all()

    contexto = {
        'pizza': pizza,
        'ingredientes': ingredientes,
    }
    return render(request, 'detalle_pizza.html', contexto)

def allpizzas(request):
    pizzas = Pizza.objects.all()

    seleccionados = []
    for valor in request.GET.getlist('ingrediente'):
        if valor.isdecimal() and int(valor) not in seleccionados:
            seleccionados.append(int(valor))

    #por cada ingrediente marcado nos quedamos solo con las pizzas que lo llevan, así que al final quedan las pizzas que llevan TODOS los ingredientes marcados
    for id_ingrediente in seleccionados:
        pizzas = pizzas.filter(ingredientes__id=id_ingrediente)

    context = {
        'pizzas': pizzas,
        'ingredientes': Ingrediente.objects.all(), #para pintar los checkbox
        'seleccionados': seleccionados, #para dejar marcados los que se han elegido
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
    return render(request, 'login.html')

def addpizza(request):
    masas = TipoMasa.objects.all()
    context = {
        'masas': masas
    }
    return render(request, "addPizzaAdmin.html", context)