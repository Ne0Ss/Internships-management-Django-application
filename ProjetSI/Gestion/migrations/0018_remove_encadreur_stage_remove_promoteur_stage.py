# Generated by Django 4.0 on 2022-01-28 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Gestion', '0017_alter_stage_rapport_alter_sujetpfe_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='encadreur',
            name='Stage',
        ),
        migrations.RemoveField(
            model_name='promoteur',
            name='Stage',
        ),
    ]
