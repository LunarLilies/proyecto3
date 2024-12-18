# Generated by Django 5.1.3 on 2024-11-24 02:44

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carrito',
            fields=[
                ('id_carrito', models.AutoField(primary_key=True, serialize=False)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id_producto', models.AutoField(primary_key=True, serialize=False)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='fotos/')),
                ('nombre_prod', models.CharField(max_length=100)),
                ('stock', models.IntegerField(default=0)),
                ('precio', models.IntegerField()),
                ('descripcion', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id_usuario', models.AutoField(primary_key=True, serialize=False)),
                ('nom_usuario', models.CharField(max_length=15)),
                ('contraseña', models.CharField(max_length=12, validators=[django.core.validators.MinLengthValidator(4)])),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CarritoProducto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cant_compra', models.IntegerField(default=1)),
                ('subtotal', models.IntegerField()),
                ('total_carro', models.IntegerField()),
                ('carrito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='carro_compra.carrito')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productos_carrito', to='carro_compra.producto')),
            ],
        ),
        migrations.AddField(
            model_name='carrito',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuario_carrito', to='carro_compra.usuario'),
        ),
    ]
