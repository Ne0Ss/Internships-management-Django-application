# Generated by Django 4.0 on 2022-01-25 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gestion', '0012_remove_etudiant_annéeetude_alter_etudiant_matricule'),
    ]

    operations = [
        migrations.AddField(
            model_name='encadreur',
            name='image',
            field=models.ImageField(default='noimg.png', upload_to=''),
        ),
    ]
