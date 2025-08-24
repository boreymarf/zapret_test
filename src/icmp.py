import subprocess
import platform

def check_icmp(hostname):
    """
    Проверка доступности через ICMP (ping)
    """
    if platform.system().lower() == 'windows':
        command = ['ping', '-n', '1', '-w', '2000', hostname]
    else:
        command = ['ping', '-c', '1', '-W', '2', hostname]
    
    try:
        result = subprocess.run(command, 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE,
                              timeout=5)
        return result.returncode == 0
    except:
        return False
