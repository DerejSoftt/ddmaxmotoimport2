# Clean up test invoice numbers

from django.db import migrations
import re


def clean_test_invoices(apps, schema_editor):
    """Remove or regenerate invoices created by test scripts with timestamp numbers"""
    Venta = apps.get_model('facturacion', 'Venta')
    
    # Find all test invoices (TEST- prefix and F-YYYY-{14 digits})
    malformed = []
    for venta in Venta.objects.all():
        if venta.numero_factura:
            # Check if it's a test invoice or F-YYYY-{14 digits timestamp}
            if venta.numero_factura.startswith('TEST-'):
                # Option 1: Delete test invoices (if they don't have associated data)
                # For safety, we'll just regenerate them
                malformed.append(venta)
            elif re.match(r'F-\d{4}-\d{14}', venta.numero_factura):
                # Regenerate F-YYYY-{timestamp} format
                malformed.append(venta)
    
    # Regenerate numbers for malformed invoices
    for venta in malformed:
        year = venta.fecha_venta.year
        
        # Get the highest sequential number for this year
        max_sequence = 0
        for other_venta in Venta.objects.filter(fecha_venta__year=year):
            if other_venta.numero_factura and other_venta.id != venta.id:
                if other_venta.numero_factura.startswith('TEST-'):
                    continue
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


def reverse_clean(apps, schema_editor):
    """Reverse is not applicable"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0029_fix_malformed_invoice_numbers'),
    ]

    operations = [
        migrations.RunPython(clean_test_invoices, reverse_clean),
    ]
