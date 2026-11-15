# Tabla Ingrediente y relación con Pizza.
#
# Antes los ingredientes de cada pizza eran un texto ("Tomate, Mozzarella, Albahaca").
# Esta migración crea la tabla Ingrediente, la relaciona con Pizza (ManyToMany) y pasa
# a la tabla nueva el texto que ya había guardado, para no perder los datos.

from django.db import migrations, models


def pasar_ingredientes_a_tabla(apps, schema_editor):
    Pizza = apps.get_model('restaurante', 'Pizza')
    Ingrediente = apps.get_model('restaurante', 'Ingrediente')

    for pizza in Pizza.objects.order_by('id'):
        # "Tomate, Mozzarella, Albahaca" --> "Tomate", "Mozzarella", "Albahaca"
        for nombre in pizza.ingredientes_texto.split(','):
            nombre = nombre.strip()
            if nombre:
                # si el ingrediente ya existe (lo lleva otra pizza) se reutiliza; si no, se crea
                ingrediente, creado = Ingrediente.objects.get_or_create(titulo=nombre)
                pizza.ingredientes.add(ingrediente)


class Migration(migrations.Migration):

    dependencies = [
        ('restaurante', '0002_user'),
    ]

    operations = [
        # 1) tabla nueva
        migrations.CreateModel(
            name='Ingrediente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'ordering': ['titulo'],
            },
        ),
        # 2) el texto antiguo se aparta con otro nombre para dejar libre "ingredientes"
        migrations.RenameField(
            model_name='pizza',
            old_name='ingredientes',
            new_name='ingredientes_texto',
        ),
        # 3) la relación nueva entre Pizza e Ingrediente
        migrations.AddField(
            model_name='pizza',
            name='ingredientes',
            field=models.ManyToManyField(to='restaurante.ingrediente'),
        ),
        # 4) se copian los datos del texto a la tabla
        migrations.RunPython(pasar_ingredientes_a_tabla),
        # 5) el texto ya no hace falta
        migrations.RemoveField(
            model_name='pizza',
            name='ingredientes_texto',
        ),
    ]
