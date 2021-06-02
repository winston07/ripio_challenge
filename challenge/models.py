from django.db import models
from datetime import datetime
from django.utils import timezone
# Create your models here.
from utils.middlewares.requests import AppRequestMiddleware
from utils.network.tracking import get_client_ip


class Moneda(models.Model):
    codigo = models.CharField(unique=True, max_length=3)
    descripcion = models.CharField(max_length=120)
    es_activo = models.BooleanField(default=True)
    es_principal = models.BooleanField(default=False)

    class Meta:
        ordering = ['codigo', 'es_activo']
        verbose_name = u'Moneda'
        verbose_name_plural = u'Monedas'

    def __str__(self):
        return self.descripcion


class TipoCambio(models.Model):
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT)
    equivalencia = models.DecimalField(max_digits=20, decimal_places=3)
    fecha = models.DateField()

    class Meta:
        unique_together = [['moneda', 'fecha']]
        ordering = ['-fecha']


class Cuenta(models.Model):
    from django.conf import settings
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT)
    nro_cuenta = models.CharField(max_length=20)
    saldo = models.DecimalField(max_digits=20, decimal_places=3)
    es_activo = models.BooleanField(default=True)


class Operacion(models.Model):
    numero_operacion = models.IntegerField()
    cuenta_origen = models.ForeignKey(Cuenta, on_delete=models.PROTECT, related_name='origen_operacion')
    cuenta_destino = models.ForeignKey(Cuenta, on_delete=models.PROTECT, related_name='destino_operacion')
    monto = models.DecimalField(max_digits=20, decimal_places=3)
    fecha_operacion = models.DateTimeField('Fecha operacion', default=timezone.now())
    ip_operacion = models.CharField(max_length=15, blank=True)

    class Meta:
        ordering = ['-fecha_operacion']

    def save(self, *args, **kwargs):
        current_request = AppRequestMiddleware.get_request()
        if current_request:
            self.ip_operacion = get_client_ip(current_request)
        super(Operacion, self).save(*args, **kwargs)


class Movimiento(models.Model):
    cuenta = models.ForeignKey(Cuenta, on_delete=models.PROTECT)
    operacion = models.ForeignKey(Operacion, on_delete=models.PROTECT)
    fecha = models.DateTimeField('Fecha movimiento', default=timezone.now())
    es_abono = models.BooleanField(default=True)

    class Meta:
        unique_together = [['operacion', 'cuenta']]
        ordering = ['-fecha']
