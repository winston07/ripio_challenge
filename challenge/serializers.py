from rest_framework import serializers
from django.utils import timezone

from challenge.models import Moneda, TipoCambio, Cuenta, Operacion, Movimiento


class MonedaSerializer(serializers.ModelSerializer):
    tipo_cambio = serializers.SerializerMethodField()

    class Meta:
        model = Moneda
        fields = '__all__'

    def get_tipo_cambio(self, obj):
        tipo_cambio = TipoCambio.objects.filter(moneda=obj.id, fecha=timezone.now()).first()
        if tipo_cambio:
            return tipo_cambio.equivalencia
        else:
            tipocambio = TipoCambio.objects.filter(moneda=obj.id).first()
            return tipocambio.equivalencia


class TipoCambioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoCambio
        fields = '__all__'


class CuentaSerializer(serializers.ModelSerializer):
    moneda_desc = serializers.SerializerMethodField()
    class Meta:
        model = Cuenta
        fields = '__all__'

    def get_moneda_desc(self,obj):
        return obj.moneda.codigo


class OperacionSerializer(serializers.ModelSerializer):
    numero_operacion = serializers.CharField(required=False)
    cuenta_origen = serializers.SerializerMethodField()
    cuenta_destino = serializers.SerializerMethodField()

    class Meta:
        model = Operacion
        fields = '__all__'

    def get_cuenta_origen(self, obj):
        return obj.cuenta_origen.id

    def get_cuenta_destino(self, obj):
        return obj.cuenta_destino.id


class MovimientoSerializer(serializers.ModelSerializer):
    numero_operacion = serializers.SerializerMethodField()
    cuenta_origen = serializers.SerializerMethodField()
    cuenta_destino = serializers.SerializerMethodField()
    monto = serializers.SerializerMethodField()
    fecha_ope = serializers.SerializerMethodField()

    class Meta:
        model = Movimiento
        fields = '__all__'

    def get_numero_operacion(self, obj):
        return obj.operacion.numero_operacion

    def get_cuenta_origen(self, obj):
        return obj.operacion.cuenta_origen.nro_cuenta

    def get_cuenta_destino(self, obj):
        return obj.operacion.cuenta_destino.nro_cuenta

    def get_monto(self, obj):
        return obj.operacion.monto

    def get_fecha_ope(self, obj):
        return obj.operacion.fecha_operacion
