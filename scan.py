from django.core.management.base import BaseCommand
from monitor.scanner import scan_network


class Command(BaseCommand):
    help = "Scan the network and save devices"

    def handle(self, *args, **kwargs):
        devices = scan_network()
        self.stdout.write(
            self.style.SUCCESS(
                f"Found {len(devices)} devices."
            )
        )