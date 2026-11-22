from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Pizza, TipoMasa, Ingrediente, User
from .forms import LoginForm
from .forms import addPizzaForm
from .models import CompraIngrediente
from .forms import CompraPizzaForm

# Create your views here.



def home(request):
    pizzas = Pizza.objects.order_by('-num_ventas')[:3]
    context = {
        'pizzas' : pizzas
    }
    return render(request, "cover.html", context)

def ingredientes_sin_stock(pizza, cantidad):
    # cada pizza gasta 1 unidad de cada uno de sus ingredientes, así que para hacer
    # 'cantidad' pizzas hacen falta 'cantidad' unidades de cada ingrediente.
    # Devuelve los nombres de los ingredientes de los que no hay suficiente (lista vacía = hay de todo)
    faltan = []
    for ingrediente in pizza.ingredientes.all():
        if ingrediente.stock < cantidad:
            faltan.append(ingrediente.titulo)
    return faltan

def filtrarpizza(request, idPizza):
    # detalle de una pizza --> /pizza/<idPizza>
    # busca la pizza por su id; si no existe, lanza Http404 automáticamente
    pizza = get_object_or_404(Pizza, pk=idPizza)

    ingredientes = pizza.ingredientes.all()

    if request.method == 'POST':
        # el cliente ha pulsado "Comprar": formulario "bound" con la cantidad que ha escrito
        form = CompraPizzaForm(request.POST)
        if form.is_valid():
            cantidad = form.cleaned_data['cantidad']

            # antes de restar nada comprobamos que hay stock de todos los ingredientes
            faltan = ingredientes_sin_stock(pizza, cantidad)
            if faltan:
                # no llega para esa cantidad: error general del formulario y no se compra nada
                form.add_error(None, 'No hay stock suficiente de: ' + ', '.join(faltan) + '.')
            else:
                # hay de todo: restamos de cada ingrediente una unidad por cada pizza comprada
                for ingrediente in ingredientes:
                    ingrediente.stock = ingrediente.stock - cantidad
                    ingrediente.save()

                # sumamos las pizzas vendidas (con esto se ordena "Las más vendidas" de la portada)
                pizza.num_ventas = pizza.num_ventas + cantidad
                pizza.save()

                # guardamos el mensaje en la sesión para enseñarlo después de redireccionar
                total = pizza.precio * cantidad
                request.session['mensaje_compra'] = f'¡Compra realizada! {cantidad} x {pizza.titulo}. Total: {total} €'

                # redireccionamos a la misma página (GET) para que al recargar no se compre otra vez
                return redirect('filtrarpizza', idPizza=pizza.id)
    else:
        # GET: formulario vacío ("unbound"), con la cantidad a 1
        form = CompraPizzaForm()

    contexto = {
        'pizza': pizza,
        'ingredientes': ingredientes,
        'form': form,
        # si falta algún ingrediente no se puede hacer ni una pizza: está agotada
        'sin_stock': ingredientes_sin_stock(pizza, 1),
        # pop saca el mensaje de la sesión y lo borra, así solo se ve una vez
        'mensaje': request.session.pop('mensaje_compra', None),
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
    # pizzas que tienen esta masa, pero solo las que se pueden hacer:
    # si a una pizza le falta stock de algún ingrediente, no se muestra
    pizzas = []
    for pizza in Pizza.objects.filter(tipo=masa):
        if not ingredientes_sin_stock(pizza, 1):
            pizzas.append(pizza)
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

def stock_ingredientes(request):
    # página del panel para ver el stock y registrar las compras de ingredientes
    # igual que el panel: si no ha iniciado sesión, lo mandamos al login
    if 'usuario_id' not in request.session:
        return redirect('login')

    ingredientes = Ingrediente.objects.all()  # salen en orden alfabético (ordering del modelo)

    if request.method == 'POST':
        num_compras = 0
        # en la tabla, la casilla de cada ingrediente se llama "cantidad_<id del ingrediente>"
        for ingrediente in ingredientes:
            valor = request.POST.get('cantidad_' + str(ingrediente.id), '')
            # solo cuentan los números enteros mayores que 0 (las casillas vacías se ignoran)
            if valor.isdecimal() and int(valor) > 0:
                cantidad = int(valor)

                # 1) registramos la compra en la tabla CompraIngrediente (la fecha se pone sola)
                compra = CompraIngrediente(ingrediente=ingrediente, cantidad=cantidad)
                compra.save()

                # 2) sumamos lo comprado al stock del ingrediente
                ingrediente.stock = ingrediente.stock + cantidad
                ingrediente.save()

                num_compras = num_compras + 1

        if num_compras > 0:
            request.session['mensaje_stock'] = f'Compras registradas: {num_compras}.'
        else:
            request.session['mensaje_stock'] = 'No has escrito ninguna cantidad.'
        # redireccionamos (GET) para que al recargar no se registren las compras otra vez
        return redirect('stock')

    context = {
        'ingredientes': ingredientes,
        'compras': CompraIngrediente.objects.order_by('-fecha')[:10],  # las 10 últimas compras
        'mensaje': request.session.pop('mensaje_stock', None),
    }
    return render(request, 'stockIngredientes.html', context)

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