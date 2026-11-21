from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Pizza, TipoMasa, Ingrediente, User
from .forms import LoginForm
from .forms import addPizzaForm

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
    if request.method == 'POST':
        # formulario "bound": le asociamos los datos que ha enviado el usuario
        form = LoginForm(request.POST)
        # validamos los datos (campos obligatorios, formato de email...)
        if form.is_valid():
            # los datos ya validados quedan en form.cleaned_data
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            usuario = User.objects.filter(email=email, password=password).first()
            if usuario:
                # guardamos en la sesión quién ha iniciado sesión
                request.session['usuario_id'] = usuario.id
                request.session['usuario_nombre'] = usuario.nombre
                # redireccionamos a otra URL (igual que HttpResponseRedirect('/'))
                return redirect('panel_admin')

            # el email o la contraseña no coinciden: error general del formulario (non_field_errors)
            form.add_error(None, 'El email o la contraseña no son correctos.')
    else:
        # si es GET (primera vez que se entra) creamos un formulario vacío, "unbound"
        form = LoginForm()

    # se pinta la plantilla con el formulario vacío o con los datos y los errores
    return render(request, 'login.html', {'form': form})

def panel_admin(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    context = {
        'nombre': request.session.get('usuario_nombre'),
    }
    return render(request, "panelAdmin.html", context)

def eliminar_pizza(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    return render(request, "eliminarPizza.html")

def logout_view(request):
    request.session.flush()
    return redirect('home')

def addpizza(request):

    masas = TipoMasa.objects.all()
    ingredientes = Ingrediente.objects.all()

    if request.method == 'POST':

        form = addPizzaForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('all_pizza')

    else:
        form = addPizzaForm()

    context = {
        'masas': masas,
        'ingredientes': ingredientes,
        'form': form
    }

    return render(request, "addPizzaAdmin.html", context)

    # masas = TipoMasa.objects.all()
    # ingredientes = Ingrediente.objects.all()
    # context = {
    #     'masas': masas,
    #     'ingredientes': ingredientes
    # }
    # return render(request, "addPizzaAdmin.html", context)