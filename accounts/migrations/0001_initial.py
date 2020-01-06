# Generated by Django 2.1.9 on 2020-01-04 09:02

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('region', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank='True', default=datetime.datetime.now)),
                ('montant', models.PositiveIntegerField()),
                ('observation', models.TextField(null='True')),
                ('user', models.ForeignKey(null='True', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telephone', models.CharField(max_length=10, null='True')),
                ('adresse', models.CharField(default='alger', max_length=325)),
                ('activate', models.CharField(max_length=255, unique='True')),
                ('solde', models.IntegerField(default=0)),
                ('user', models.OneToOneField(null='True', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('wilaya', models.ForeignKey(null='true', on_delete=django.db.models.deletion.CASCADE, to='region.Wilaya')),
            ],
        ),
    ]