# Generated by Django 4.2 on 2023-04-17 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0009_remove_tour_image_imagetour'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagetour',
            name='image',
            field=models.ImageField(null=True, upload_to='images/tours/%Y/%m/'),
        ),
    ]