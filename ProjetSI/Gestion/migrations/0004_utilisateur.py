# Generated by Django 4.0 on 2022-01-23 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gestion', '0003_etudiant_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('identifiant', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('mdp', models.CharField(max_length=20)),
            ],
        ),
    ]
