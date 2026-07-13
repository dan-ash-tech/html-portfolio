
from django.db import models


class Device(models.Model):

    hostname = models.CharField(max_length=100, blank=True)

    ip_address = models.GenericIPAddressField(unique=True)

    mac_address = models.CharField(max_length=50, unique=True)

    vendor = models.CharField(max_length=100, blank=True)

    first_seen = models.DateTimeField(auto_now_add=True)

    last_seen = models.DateTimeField(auto_now=True)

    online = models.BooleanField(default=True)

    is_new = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.hostname} - {self.ip_address}"
