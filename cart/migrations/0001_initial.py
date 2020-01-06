# Generated by Django 2.1.9 on 2020-01-04 09:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('produits', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('session_key', models.CharField(max_length=40)),
                ('user', models.OneToOneField(default=None, null='True', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.PositiveIntegerField()),
                ('qtt', models.PositiveIntegerField()),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.Cart')),
                ('product_with_attribute', models.ForeignKey(blank='true', null='true', on_delete=django.db.models.deletion.CASCADE, to='produits.ProductAttribute')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produits.Produit')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='cart',
            unique_together={('user', 'session_key')},
        ),
    ]