# Generated by Django 4.1.3 on 2022-11-12 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='dateTime',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
