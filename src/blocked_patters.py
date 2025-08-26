BLOCKED_HOSTNAME_PATTERNS = [
    r"perm\.ertelecom\.ru$"
]


def is_blocked_hostname(hostname):
    """Check if hostname matches known blocking patterns"""
    import re
    if hostname is None or hostname == "":
        return False
    for pattern in BLOCKED_HOSTNAME_PATTERNS:
        if re.search(pattern, hostname):
            return True
    return False
