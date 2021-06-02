# Generated by Django 3.2.3 on 2021-06-02 03:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0003_auto_20210602_0323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimiento',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 2, 3, 53, 7, 447988, tzinfo=utc), verbose_name='Fecha movimiento'),
        ),
        migrations.AlterField(
            model_name='operacion',
            name='fecha_operacion',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 2, 3, 53, 7, 447204, tzinfo=utc), verbose_name='Fecha operacion'),
        ),
        migrations.AlterField(
            model_name='operacion',
            name='ip_operacion',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
