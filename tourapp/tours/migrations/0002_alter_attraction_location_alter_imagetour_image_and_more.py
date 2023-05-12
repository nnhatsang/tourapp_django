# Generated by Django 4.2 on 2023-05-09 09:28

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attraction',
            name='location',
            field=models.CharField(default='none', max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='imagetour',
            name='image',
            field=cloudinary.models.CloudinaryField(default='', max_length=255, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='imagetour',
            name='tour',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tours.tour'),
        ),
        migrations.AlterField(
            model_name='tour',
            name='image',
            field=cloudinary.models.CloudinaryField(default='', max_length=255, null=True, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=cloudinary.models.CloudinaryField(default='', max_length=255, null=True, verbose_name='avatar'),
        ),
    ]