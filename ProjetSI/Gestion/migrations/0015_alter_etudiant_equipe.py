# Generated by Django 4.0 on 2022-01-27 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Gestion', '0014_sujetpfe_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='etudiant',
            name='Equipe',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='Gestion.equipe'),
            preserve_default=False,
        ),
    ]
