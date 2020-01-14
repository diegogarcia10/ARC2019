# Generated by Django 2.0.5 on 2020-01-14 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cita',
            name='asistio',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='resetamedica',
            name='cod_reseta',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
