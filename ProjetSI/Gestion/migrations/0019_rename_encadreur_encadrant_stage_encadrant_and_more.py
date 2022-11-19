# Generated by Django 4.0 on 2022-01-28 23:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Gestion', '0018_remove_encadreur_stage_remove_promoteur_stage'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Encadreur',
            new_name='Encadrant',
        ),
        migrations.AddField(
            model_name='stage',
            name='Encadrant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Gestion.encadrant'),
        ),
        migrations.AddField(
            model_name='stage',
            name='Promoteur',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Gestion.promoteur'),
        ),
    ]
