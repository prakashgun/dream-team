# Generated by Django 3.1.2 on 2020-10-24 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('performance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerstats',
            name='highest_score',
            field=models.CharField(max_length=10),
        ),
    ]