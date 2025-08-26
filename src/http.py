from src.blocked_patters import is_blocked_hostname

from aiohttp import ClientSession, ClientTimeout
from aiohttp import TCPConnector

import asyncio
import socket


async def check_http(domain_name):
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
            max_field_size=16380,
            connector=TCPConnector(ssl=False)
        ) as session:
            async with session.get(f"http://{domain_name}") as resp:
                if resp.status == 200:

                    if is_blocked_hostname(host_name):
                        print(f"{domain_name:20} | HTTP  | Blocked")
                    else:
                        print(f"{domain_name:20} | HTTP  | OK")

                elif resp.status == 403:
                    print(f"{domain_name:20} | HTTP  | Forbidden")
                elif resp.status == 503:
                    print(f"{domain_name:20} | HTTP  | Unreachable")
                else:
                    print(f"{domain_name:20} | HTTP  | {resp.status}")

    except TimeoutError:
        print(f"{domain_name:20} | HTTP  | Timeout")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise
