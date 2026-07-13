from django.shortcuts import render, redirect
from .models import Device
from .scanner import scan_network


scan_results = {
    "new_devices": [],
    "existing_devices": [],
}




def dashboard(request):

    devices = Device.objects.all().order_by("ip_address")

    context = {
        "devices": devices,
        "total_devices": devices.count(),
        "online_devices": devices.filter(online=True).count(),
        "offline_devices": devices.filter(online=False).count(),
        "new_devices": devices.filter(is_new=True),
        "existing_devices": devices.filter(is_new=False),
        "total_devices": devices.count(),




    }

    return render(request, "monitor/dashboard.html", context)

def scan_network_view(request):
    if request.method == "POST":
        scan_network()
        scan_results = scan_network()

    return redirect("dashboard")
