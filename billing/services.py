from django.db import transaction
from django.db.models import F

from inventory.models import StockMovement
from shared.money import round_money


def recalc_invoice(invoice):
    """Recalcula subtotal/IVA/total de una factura a partir de sus líneas."""
    details          = list(invoice.details.all())
    invoice.subtotal = round_money(sum(d.subtotal   for d in details))
    invoice.tax      = round_money(sum(d.tax_amount for d in details))
    invoice.total    = round_money(invoice.subtotal + invoice.tax)
    invoice.save()


def check_stock(invoice):
    """Devuelve la lista de errores de stock insuficiente (vacía si hay stock para todo)."""
    details = list(invoice.details.select_related('product').all())
    return [
        f'{d.product.name}: disponible {d.product.stock}, requerido {d.quantity}'
        for d in details if d.product.stock < d.quantity
    ]


def emit_invoice(invoice, user):
    """Emite una factura en Borrador: descuenta stock y registra StockMovement.

    Usado tanto por billing.views.invoice_confirm (emisión manual por el
    Vendedor) como por el checkout de la tienda (store.views), para no
    duplicar la lógica de descuento de stock y auditoría.
    """
    from .models import Invoice, Product

    details = list(invoice.details.select_related('product').all())
    with transaction.atomic():
        for detail in details:
            Product.objects.filter(pk=detail.product_id).update(
                stock=F('stock') - detail.quantity
            )
        StockMovement.objects.bulk_create([
            StockMovement(
                product_id=detail.product_id,
                quantity=-detail.quantity,
                movement_type=StockMovement.VENTA,
                user=user,
                invoice=invoice,
            )
            for detail in details
        ])
        invoice.estado = Invoice.EMITIDA
        invoice.save()
