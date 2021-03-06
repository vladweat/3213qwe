# Generated by Django 4.0.4 on 2022-05-22 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web3app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='description',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='end_date',
            field=models.DateTimeField(default=None),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='long_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='short_name',
            field=models.CharField(max_length=100),
        ),
    ]
