# Generated by Django 2.1.2 on 2018-11-25 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='number',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tag',
            name='number',
            field=models.IntegerField(default=0),
        ),
    ]