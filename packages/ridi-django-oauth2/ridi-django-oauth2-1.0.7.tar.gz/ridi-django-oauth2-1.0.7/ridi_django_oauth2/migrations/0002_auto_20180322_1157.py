# Generated by Django 2.0.2 on 2018-03-22 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ridi_django_oauth2', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ridiuser',
            name='u_idx',
            field=models.IntegerField(editable=False, primary_key=True, serialize=False, verbose_name='u_idx'),
        ),
    ]
