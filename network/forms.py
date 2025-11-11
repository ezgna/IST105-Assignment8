from django import forms
import re

MAC_RE = re.compile(r'^[0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5}$')

class LeaseRequestForm(forms.Form):
    mac_address = forms.CharField(
        label="MAC Address",
        max_length=17,
        help_text="例: 00:1A:2B:3C:4D:5E"
    )
    DHCP_CHOICES = [('DHCPv4', 'DHCPv4'), ('DHCPv6', 'DHCPv6')]
    dhcp_version = forms.ChoiceField(choices=DHCP_CHOICES, label="DHCP Version")

    def clean_mac_address(self):
        mac = self.cleaned_data['mac_address'].strip()
        if not MAC_RE.match(mac):
            raise forms.ValidationError("フォーマットエラー: 6オクテットの16進数をコロン区切りで。")
        return mac.upper()