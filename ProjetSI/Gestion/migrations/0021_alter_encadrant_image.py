# Generated by Django 4.0 on 2022-01-29 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gestion', '0020_alter_encadrant_image_alter_etudiant_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encadrant',
            name='image',
            field=models.ImageField(default='encadrants/images/noimg.png', upload_to='encadrants/images/'),
        ),
    ]
