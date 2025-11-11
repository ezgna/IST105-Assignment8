import ipaddress

def mac_bytes(mac: str):
    return [int(x, 16) for x in mac.split(':')]

def mac_to_ipv4(mac: str) -> str:
    # 192.168.1.10〜250の範囲で、MACごとに決定的な値を割り当て
    b = mac_bytes(mac)
    s = sum(b)
    host = 10 + (s % 241)  # 10..250
    return f"192.168.1.{host}"

def mac_to_eui64_ipv6(mac: str, prefix: str = '2001:db8::/64') -> str:
    # EUI-64生成:
    # 1) 先頭バイトのU/Lビットを反転: b0 ^ 0x02
    # 2) 中央に ff:fe を挿入
    b = mac_bytes(mac)
    b[0] ^= 0x02
    eui = b[:3] + [0xFF, 0xFE] + b[3:]
    iid = int.from_bytes(bytes(eui), 'big')

    net = ipaddress.IPv6Network(prefix, strict=False)
    addr = int(net.network_address) | iid
    return str(ipaddress.IPv6Address(addr))

def bitwise_checks(mac: str) -> dict:
    # 合計値が偶数か奇数か（& 1 で判定）、U/Lビット反転後の先頭バイト表示
    b = mac_bytes(mac)
    s = sum(b)
    sum_is_even = (s & 1) == 0
    toggled_first = b[0] ^ 0x02
    return {
        "mac_byte_sum": s,
        "sum_is_even": sum_is_even,
        "first_byte_after_toggle": f"{toggled_first:02x}",
    }