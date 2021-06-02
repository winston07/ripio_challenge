from django.contrib import admin

# Register your models here.
from challenge.models import Moneda, TipoCambio, Cuenta, Operacion, Movimiento

admin.site.register(Moneda)
admin.site.register(TipoCambio)
admin.site.register(Cuenta)
admin.site.register(Operacion)
admin.site.register(Movimiento)
