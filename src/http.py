import requests
from requests.exceptions import SSLError, Timeout, ConnectionError


def check_http(hostname):
    try:
        response = requests.get(f"https://{hostname}", timeout=2)
        status = response.status_code
        return status == 200
    except (Timeout, ConnectionError, SSLError):
        return False
    except Exception as e:
        raise e
