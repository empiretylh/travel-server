# Generated by Django 3.2.9 on 2023-03-17 22:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20230315_2322'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='paymentinfo',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='paymentinfo', to='app.paymentinfo'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
