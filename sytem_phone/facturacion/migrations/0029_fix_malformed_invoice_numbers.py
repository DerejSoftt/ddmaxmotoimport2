# Generated migration to fix malformed invoice numbers

from django.db import migrations
import re
from decimal import Decimal


def fix_invoice_numbers(apps, schema_editor):
    """Fix invoice numbers that were generated with timestamps instead of sequences"""
    Venta = apps.get_model('facturacion', 'Venta')
    
    # Find all invoices with malformed numbers (F-YYYY-{timestamp})
    # Pattern: F-20XX-20XX04... (timestamp pattern)
    malformed = []
    for venta in Venta.objects.all():
        if venta.numero_factura:
            # Check if it matches F-YYYY-{14 digit timestamp}
            match = re.match(r'F-(\d{4})-(\d{14})', venta.numero_factura)
            if match:
                malformed.append(venta)
    
    # For each malformed entry, generate a new proper number
    for venta in malformed:
        year = venta.fecha_venta.year
        
        # Get the highest sequential number for this year
        max_sequence = 0
        for other_venta in Venta.objects.filter(fecha_venta__year=year):
            if other_venta.numero_factura:
                match = re.match(r'F-\d{4}-(\d+)', other_venta.numero_factura)
                if match:
                    try:
                        seq = int(match.group(1))
                        if seq > max_sequence:
                            max_sequence = seq
                    except ValueError:
                        pass
        
        # Generate new number
        new_number = max_sequence + 1
        new_numero_factura = f"F-{year}-{new_number:06d}"
        
        # Update the venta
        venta.numero_factura = new_numero_factura
        venta.save(update_fields=['numero_factura'])


def reverse_fix(apps, schema_editor):
    """Reverse is not applicable for this fix"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0028_alter_venta_numero_factura'),
    ]

    operations = [
        migrations.RunPython(fix_invoice_numbers, reverse_fix),
    ]
