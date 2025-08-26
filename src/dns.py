import dns.resolver

ipv4_dns = {
    "cloudflare": [
        "1.1.1.1",
        "1.0.0.1"
    ],
    "google": [
        "8.8.8.8",
        "8.8.4.4"
    ],
    "yandex": [
        "77.88.8.8",
        "77.88.8.1"
    ]
}

ipv6_dns = {
    "cloudflare": [
        "2606:4700:4700::1111",
        "2606:4700:4700::1001"
    ],
    "google": [
        "2001:4860:4860::8888",
        "2001:4860:4860::8844"
    ],
    "yandex": [
        "2a02:6b8::feed:0ff",
        "2a02:6b8:0:1::feed:0ff"
    ]
}


def check_dns():
    ips = dns.resolver.Resolver().nameservers
    return is_known_ipv4_dns(ips[0])


def is_known_ipv4_dns(ip):

    if ip == "":
        return None

    for provider, ips in ipv4_dns.items():
        if ip in ips:
            return provider

    return None


# Is not used, since I don't know how to get IPv6 DNS ip yet.
def is_known_ipv6_dns(ip):

    if ip == "":
        return None

    for provider, ips in ipv6_dns.items():
        if ip in ips:
            return provider

    return None
