# Generated by Django 4.0.4 on 2022-12-09 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_userdetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='hasHouses',
            field=models.BooleanField(default=False),
        ),
    ]
