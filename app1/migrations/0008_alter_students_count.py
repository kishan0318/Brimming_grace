# Generated by Django 4.1.3 on 2022-11-12 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0007_students_course_students_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='count',
            field=models.IntegerField(default=1),
        ),
    ]