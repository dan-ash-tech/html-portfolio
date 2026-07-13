import socket 
from scapy.all import ARP, Ether, srp
from .models import Device

def get_vendor(mac):
    # Placeholder implementation - replace with actual vendor lookup logic
    return "Unknown Vendor"

def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return "Unknown"
    
def scan_network():

    # CHANGE THIS TO YOUR NETWORK
    network = "10.10.20.0/24"

    print("Scanning network...")

    arp_request = ARP(
        pdst=network
    )

    broadcast = Ether(
        dst="ff:ff:ff:ff:ff:ff"
    )

    packet = broadcast / arp_request

    answered = srp(
        packet,
        timeout=3,
        verbose=False
    )[0]

    discovered_devices = []
    new_devices = []
    existing_devices = []
    active_macs = set()

    for sent, received in answered:
        ip = received.psrc
        mac = received.hwsrc
        active_macs.add(mac)
        hostname = get_hostname(ip)

        device, created = Device.objects.update_or_create(
            mac_address=mac,
            defaults={
                "ip_address": ip,
                "hostname": hostname,
                "online": True,
                
            }
           
        )

        



        discovered_devices.append(device)

        if created:
            new_devices.append((ip, mac, hostname))
        else:
           existing_devices.append((ip, mac, hostname))

        if created:
                device.is_new = True
        else:
                device.is_new = False

                device.save()



    
    from django.utils import timezone
    from datetime import timedelta


    Device.objects.exclude(
    mac_address__in=active_macs
    ).update(
    online=False
    )




    print("\n=== Existing Devices ===")
    for ip, mac, hostname in existing_devices:
        print(f"{ip} | {hostname} | {mac}")

    print("\n=== New Devices ===")
    for ip, mac, hostname in new_devices:
        print(f"{ip} | {hostname} | {mac}")

    print(f"\nFound {len(discovered_devices)} devices.")
    print(f"Existing: {len(existing_devices)}")
    print(f"New: {len(new_devices)}")

    return {
    "devices": discovered_devices,
    "new_devices": new_devices,
    "existing_devices": existing_devices,
}