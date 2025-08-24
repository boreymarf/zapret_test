import requests

def check_https(hostname):
    response = requests.get(f"https://{hostname}", timeout=2)
    status = response.status_code
    return status
