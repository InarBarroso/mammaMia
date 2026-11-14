from django.urls import path
from .views import home, filtrarpizza, allpizzas, allmasas, filtrarmasa, login_view

urlpatterns = [
    path('', home, name='home'),
    # detalle de una pizza, p.ej. /pizza/3  (cover.html enlaza con {% url 'filtrarpizza' pizza.id %})
    path('pizza/<int:idPizza>', filtrarpizza, name='filtrarpizza'),
    path('all_pizza', allpizzas, name='all_pizza'),
    path('all_masas', allmasas, name='all_masas'),
    path('masa/<int:idMasa>', filtrarmasa, name='filtrarmasa'),
    # inicio de sesión (index.html enlaza con {% url 'login' %})
    path('login', login_view, name='login'),
]
