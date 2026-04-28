from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from facturacion.models import IdempotencyLog

class Command(BaseCommand):
    help = 'Limpia los logs de idempotencia antiguos (mas de 24 horas)'

    def handle(self, *args, **options):
        limite = timezone.now() - timedelta(hours=24)
        eliminados, _ = IdempotencyLog.objects.filter(created_at__lt=limite).delete()
        self.stdout.write(self.style.SUCCESS(f'Se eliminaron {eliminados} logs de idempotencia antiguos.'))
