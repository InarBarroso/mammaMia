from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurante', '0005_ingrediente_stock_compraingrediente'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='email',
            new_name='usuario',
        ),
        migrations.AlterField(
            model_name='user',
            name='usuario',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
