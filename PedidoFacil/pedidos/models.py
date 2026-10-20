from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Pedido(models.Model):
    PENDIENTE = "pendiente"
    CONFIRMADO = "confirmado"
    CANCELADO = "cancelado"
    ESTADOS = [
        (PENDIENTE, "Pendiente"),
        (CONFIRMADO, "Confirmado"),
        (CANCELADO, "Cancelado"),
    ]

    numero_pedido = models.CharField(max_length=20, unique=True)
    cliente = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(max_length=500)
    valor_total = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    estado = models.CharField(max_length=12, choices=ESTADOS, default=PENDIENTE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="pedidos")

    class Meta:
        ordering = ["-fecha_registro"]

    def __str__(self):
        return f"{self.numero_pedido} - {self.cliente}"

    @property
    def se_puede_eliminar(self):
        """Regla de negocio: un pedido confirmado no se elimina."""
        return self.estado != self.CONFIRMADO
