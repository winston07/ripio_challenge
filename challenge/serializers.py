from rest_framework import serializers

from challenge.models import Moneda, TipoCambio, Cuenta, Operacion, Movimiento


class MonedaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moneda
        fields = '__all__'


class TipoCambioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoCambio
        fields = '__all__'


class CuentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuenta
        fields = '__all__'


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
    class Meta:
        model = Movimiento
        fields = '__all__'
