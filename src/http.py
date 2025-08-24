import requests

def check_http(hostname):
    response = requests.get(f"http://{hostname}", timeout=2)
    status = response.status_code
    return status
