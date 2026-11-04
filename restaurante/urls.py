from django.urls import path
from .views import filtrarpizza

urlpatterns = [
    # detalle de una pizza, p.ej. /pizza/3  (cover.html enlaza con {% url 'filtrarpizza' pizza.id %})
    path('pizza/<int:idPizza>', filtrarpizza, name='filtrarpizza'),
]
