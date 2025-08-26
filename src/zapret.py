import subprocess
import platform
import psutil


def check_zapret():

    if platform.system().lower() == 'windows':
        # TODO: Посмотреть что он возвращает
        command = ["sc", "query", "zapret.service"]
    else:
        command = ["systemctl", "is-active", "zapret.service"]

    try:
        result = subprocess.run(command, capture_output=True, text=True)
        service_active = result.stdout.strip() == "active"
    except Exception as e:
        print(f"Exception occured! {e}")
        service_active = False

    target_names = ["zapret", "winws.exe"]
    process_found = any(proc.info['name'] and proc.info['name'].lower() in target_names
                        for proc in psutil.process_iter(['name']))

    return service_active or process_found
