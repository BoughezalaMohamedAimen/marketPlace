# Generated by Django 2.1.9 on 2020-01-04 09:02

import ckeditor.fields
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produits.Attribute')),
            ],
        ),
        migrations.CreateModel(
            name='Motif',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(blank='True', default='reference', max_length=255)),
                ('prix', models.PositiveIntegerField(blank='True', null='True')),
                ('stock', models.PositiveIntegerField(blank='True', default=0)),
                ('attributevalues', models.ManyToManyField(to='produits.AttributeValue')),
            ],
        ),
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank='True', default=datetime.datetime.now)),
                ('updated', models.DateTimeField(blank='True', default=datetime.datetime.now)),
                ('reference', models.CharField(blank='True', default='reference', max_length=255)),
                ('nom', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank='True', max_length=255)),
                ('valid', models.BooleanField(default=False)),
                ('description', ckeditor.fields.RichTextField()),
                ('seo', models.CharField(blank='True', max_length=255, null='True')),
                ('prix', models.PositiveIntegerField(default=0)),
                ('stock', models.PositiveIntegerField(null='True')),
                ('prix_promotionel', models.PositiveIntegerField(default=0)),
                ('image', models.ImageField(blank='True', null='True', upload_to='product')),
                ('image2', models.ImageField(blank='True', null='True', upload_to='product')),
                ('image3', models.ImageField(blank='True', null='True', upload_to='product')),
                ('image4', models.ImageField(blank='True', null='True', upload_to='product')),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.Categorie')),
                ('motif', models.ForeignKey(blank='True', null='True', on_delete=django.db.models.deletion.CASCADE, to='produits.Motif')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='productattribute',
            name='produit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produits.Produit'),
        ),
    ]