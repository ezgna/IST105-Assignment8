from datetime import datetime, timedelta, timezone
from django.shortcuts import render
from .forms import LeaseRequestForm
from .utils import mac_to_ipv4, mac_to_eui64_ipv6, bitwise_checks
from .mongo import get_collection

LEASE_SECONDS = 3600  # 1時間
# メモリ内リース: { mac: { "ip": str, "dhcp": "DHCPv4|DHCPv6", "expires": datetime } }
leases = {}

def home(request):
    if request.method == 'POST':
        form = LeaseRequestForm(request.POST)
        if form.is_valid():
            mac = form.cleaned_data['mac_address']
            dhcp = form.cleaned_data['dhcp_version']
            now = datetime.now(timezone.utc)

            # まだ有効期限内かつ同じDHCPなら再利用
            entry = leases.get(mac)
            if entry and entry['dhcp'] == dhcp and entry['expires'] > now:
                assigned_ip = entry['ip']
            else:
                if dhcp == 'DHCPv4':
                    assigned_ip = mac_to_ipv4(mac)
                else:
                    assigned_ip = mac_to_eui64_ipv6(mac, '2001:db8::/64')

                leases[mac] = {"ip": assigned_ip, "dhcp": dhcp, "expires": now + timedelta(seconds=LEASE_SECONDS)}

            checks = bitwise_checks(mac)
            doc = {
                "mac_address": mac,
                "dhcp_version": dhcp,
                "assigned_ip": assigned_ip,
                "lease_time": f"{LEASE_SECONDS} seconds",
                "timestamp": now.isoformat(),
                "lease_expires_at": (now + timedelta(seconds=LEASE_SECONDS)).isoformat(),
                "bitwise": checks,
            }
            # MongoDBに保存
            coll = get_collection()
            coll.insert_one(doc)

            return render(request, 'network/result.html', {"doc": doc, "checks": checks, "lease_seconds": LEASE_SECONDS})
    else:
        form = LeaseRequestForm()
    return render(request, 'network/form.html', {"form": form})

def leases_view(request):
    coll = get_collection()
    items = list(coll.find().sort("timestamp", -1))
    return render(request, 'network/leases.html', {"items": items})