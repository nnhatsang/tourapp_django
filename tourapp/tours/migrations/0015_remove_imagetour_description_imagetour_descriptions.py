# Generated by Django 4.2 on 2023-04-19 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0014_imagetour_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagetour',
            name='description',
        ),
        migrations.AddField(
            model_name='imagetour',
            name='descriptions',
            field=models.CharField(max_length=255, null=True),
        ),
    ]