from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers
from django.utils import timezone

from challenge.models import Moneda, Movimiento, TipoCambio, Cuenta, Operacion
from challenge.serializers import MonedaSerializer, TipoCambioSerializer, CuentaSerializer, OperacionSerializer, \
    MovimientoSerializer


class MonedaViewSet(viewsets.ModelViewSet):
    queryset = Moneda.objects.all()
    serializer_class = MonedaSerializer


class TipoCambioViewSet(viewsets.ModelViewSet):
    queryset = TipoCambio.objects.all()
    serializer_class = TipoCambioSerializer


class CuentaViewSet(viewsets.ModelViewSet):
    queryset = Cuenta.objects.all()
    serializer_class = CuentaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.cuenta_set.all()


class OperacionViewSet(viewsets.ModelViewSet):
    queryset = Operacion.objects.all()
    serializer_class = OperacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        operation = Operacion.objects.filter(Q(cuenta_origen__usuario=user) | Q(cuenta_destino__usuario=user))
        return operation

    def crear_op_destino(self, operacion):
        cuenta = Cuenta.objects.get(pk=operacion.cuenta_destino.id)
        if cuenta.moneda.codigo == operacion.cuenta_origen.moneda.codigo:
            cuenta.saldo += operacion.monto
            cuenta.save()
        else:
            if cuenta.moneda.codigo == 'USD' and operacion.cuenta_origen.moneda.codigo == 'PEN':
                tipocambio = TipoCambio.objects.filter(moneda=cuenta.moneda.id, fecha=timezone.now()).first()
                if tipocambio:
                    monto_ope = operacion.monto / tipocambio.equivalencia
                    cuenta.saldo += monto_ope
                    cuenta.save()
                else:
                    tipocambio = TipoCambio.objects.filter(moneda=cuenta.moneda.id).first()
                    monto_ope = operacion.monto / tipocambio.equivalencia
                    cuenta.saldo += monto_ope
                    cuenta.save()
            if cuenta.moneda.codigo == 'PEN' and operacion.cuenta_origen.moneda.codigo == 'USD':
                tipocambio = TipoCambio.objects.filter(moneda=cuenta.moneda.id, fecha=timezone.now()).first()
                if tipocambio:
                    monto_ope = operacion.monto * tipocambio.equivalencia
                    cuenta.saldo += monto_ope
                    cuenta.save()
                else:
                    tipocambio = TipoCambio.objects.filter(moneda=cuenta.moneda.id).first()
                    monto_ope = operacion.monto * tipocambio.equivalencia
                    cuenta.saldo += monto_ope
                    cuenta.save()
        data = {'cuenta': operacion.cuenta_destino.id, 'operacion': operacion.id}
        s = MovimientoSerializer(data=data)
        if s.is_valid():
            s.save()

    def crear_op_origen(self, operacion):
        cuenta = Cuenta.objects.get(pk=operacion.cuenta_origen.id)
        cuenta.saldo -= operacion.monto
        cuenta.save()
        data = {'cuenta': operacion.cuenta_origen.id, 'operacion': operacion.id, 'es_abono': False}
        s = MovimientoSerializer(data=data)
        if s.is_valid():
            s.save()

    def perform_create(self, serializer):
        data = self.request.data
        user = self.request.user
        busqueda_cta_origen = Cuenta.objects.filter(nro_cuenta=data['cuenta_origen'], usuario=user).first()
        busqueda_cta_destino = Cuenta.objects.filter(nro_cuenta=data['cuenta_destino']).first()
        if busqueda_cta_origen is None:
            content = {'mensaje': 'La cuenta origen no le pertenece o no existe', "status": status.HTTP_400_BAD_REQUEST}
            raise serializers.ValidationError(content)
        if busqueda_cta_destino is None:
            content = {'mensaje': 'La cuenta destino no existe', "status": status.HTTP_400_BAD_REQUEST}
            raise serializers.ValidationError(content)
        if float(busqueda_cta_origen.saldo) >= float(data['monto']):
            from sequences import get_next_value
            x = get_next_value()
            data = serializer.save(cuenta_origen=busqueda_cta_origen, cuenta_destino=busqueda_cta_destino,
                                   numero_operacion=x)
            self.crear_op_origen(data)
            self.crear_op_destino(data)
            super().perform_create(serializer)
        else:
            content = {'mensaje': 'No tiene saldo para hacer la transferencia', "status": status.HTTP_400_BAD_REQUEST}
            raise serializers.ValidationError(content)


class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        operation = Movimiento.objects.filter(Q(cuenta__usuario=user))
        return operation
