# Generated by Django 4.1.6 on 2023-02-04 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_delete_gamedetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='img',
            field=models.TextField(blank=True, null=True),
        ),
    ]
