# Generated by Django 4.0 on 2022-01-24 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Gestion', '0006_alter_etudiant_matricule'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipe',
            name='NbEtudEq',
        ),
    ]
