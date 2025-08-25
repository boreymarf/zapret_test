from src.blocked_patters import is_blocked_hostname

from aiohttp import ClientSession, ClientTimeout, ClientConnectorError
from aiohttp.client_exceptions import ClientConnectorCertificateError

import socket
import asyncio


async def check_https(domain_name):
    try:

        ip_address = await asyncio.to_thread(socket.gethostbyname, domain_name)

        try:
            host_name = await asyncio.to_thread(socket.gethostbyaddr, ip_address)
            host_name = host_name[0]
        except socket.herror:
            host_name = "N/A"

        async with ClientSession(
            timeout=ClientTimeout(2),
            max_line_size=16380,
            max_field_size=16380
        ) as session:
            async with session.get(f"https://{domain_name}") as resp:
                if resp.status == 200:
                    print(f"{domain_name:20} | HTTP  | OK")
                elif resp.status == 503:
                    print(f"{domain_name:20} | HTTP  | Unreachable")
                else:
                    print(f"{domain_name:20} | HTTP  | {resp.status}")

    except TimeoutError:
        print(f"{domain_name:20} | HTTPS | Timeout")
    except ClientConnectorCertificateError:
        print(f"{domain_name:20} | HTTPS | Bad certificate")
    except ClientConnectorError as e:

        if is_blocked_hostname(host_name):
            print(f"{domain_name:20} | HTTPS | Blocked")
            return

        print(f"{domain_name:20} | HTTPS | Connection error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise
