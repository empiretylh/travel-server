# Generated by Django 4.1.5 on 2023-01-30 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_feedback_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyname', models.CharField(max_length=255)),
                ('phoneno', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('image', models.ImageField(null=True, upload_to='img/companyimage/%y%mm/%dd')),
                ('companyaddress', models.TextField()),
            ],
        ),
    ]
