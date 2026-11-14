from django.db import models

class TipoMasa(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    foto = models.CharField(max_length=255)

    def __str__(self):
        return self.titulo

class Pizza(models.Model):
    titulo = models.CharField(max_length=100)
    foto = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    descripcion = models.TextField()
    tipo = models.ForeignKey(
        TipoMasa,
        on_delete=models.PROTECT,  # Si queremos borrar una masa, no debe existir ninguna pizza con esa masa asociada.
    )
    ingredientes = models.TextField()
    num_ventas = models.IntegerField(default=0)

    def __str__(self):
        return self.titulo


class User(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre