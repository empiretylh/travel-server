# Generated by Django 3.2.9 on 2023-03-20 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20230320_1330'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='is_cancel',
            field=models.BooleanField(default=False),
        ),
    ]