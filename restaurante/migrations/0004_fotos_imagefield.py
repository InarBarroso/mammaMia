# Fotos como ImageField (antes CharField).
#
# Antes "foto" guardaba la ruta dentro de static:      "img/pizzas/margarita.jpg"
# Con ImageField la ruta es relativa a MEDIA_ROOT:      "pizzas/margarita.jpg"
# Por eso, además de cambiar el tipo del campo, hay que quitar el "img/" de las rutas
# que ya estaban guardadas. (Las imágenes están ahora en media/pizzas/ y media/masas/.)

from django.db import migrations, models


def quitar_img_de_las_rutas(apps, schema_editor):
    for nombre_modelo in ['Pizza', 'TipoMasa']:
        Modelo = apps.get_model('restaurante', nombre_modelo)
        for objeto in Modelo.objects.filter(foto__startswith='img/'):
            objeto.foto = objeto.foto[len('img/'):]
            objeto.save()


class Migration(migrations.Migration):

    dependencies = [
        ('restaurante', '0003_ingredientes'),
    ]

    operations = [
        # 1) se corrigen las rutas guardadas (aquí "foto" todavía es un CharField)
        migrations.RunPython(quitar_img_de_las_rutas),
        # 2) se cambia el tipo de los campos
        migrations.AlterField(
            model_name='pizza',
            name='foto',
            field=models.ImageField(upload_to='pizzas/'),
        ),
        migrations.AlterField(
            model_name='tipomasa',
            name='foto',
            field=models.ImageField(upload_to='masas/'),
        ),
    ]
