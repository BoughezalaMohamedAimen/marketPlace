# Generated by Django 2.1.9 on 2020-01-05 06:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('region', '0002_remove_commune_code'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='commune',
            field=models.ForeignKey(null='true', on_delete=django.db.models.deletion.CASCADE, to='region.Commune'),
            preserve_default='true',
        ),
    ]
