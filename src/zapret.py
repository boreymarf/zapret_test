import subprocess
import platform

def check_zapret():

    if platform.system().lower() == 'windows':
        # TODO: Посмотреть что он возвращает
        command = ["sc", "query", "zapret.service"]
    else:
        command = ["systemctl", "is-active", "zapret.service"]

    try:
        result = subprocess.run(command, capture_output=True, text=True)
        return result.stdout.strip() == "active"
    except Exception as e:
        return e
