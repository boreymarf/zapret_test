from src.blocked_patters import is_blocked_hostname

from aiohttp import ClientSession, ClientTimeout
from aiohttp import TCPConnector
from dataclasses import dataclass

import asyncio
import socket
import logging

@dataclass
class HttpCheckResult:
    success: bool
    details: str | None


async def check_http(domain_name):
    host_name = None

    try:
        ip_address = await asyncio.to_thread(socket.gethostbyname, domain_name)

        try:
            host_name = await asyncio.to_thread(socket.gethostbyaddr, ip_address)
            host_name = host_name[0]
        except (socket.herror):
            pass

        async with ClientSession(
            timeout=ClientTimeout(2),
            max_line_size=16380,
            max_field_size=16380,
            connector=TCPConnector(ssl=False)
        ) as session:
            async with session.get(f"http://{domain_name}") as resp:
                if resp.status == 200:
                    if is_blocked_hostname(host_name):
                        logging.info(f"{domain_name:20} | HTTP  | Blocked")
                        return HttpCheckResult(
                            success=False,
                            details="Blocked by redirect"
                        )
                    else:
                        logging.info(f"{domain_name:20} | HTTP  | OK")
                        return HttpCheckResult(
                            success=True,
                            details=None
                        )
                elif resp.status == 403:
                    logging.info(f"{domain_name:20} | HTTP  | Forbidden")
                    return HttpCheckResult(
                        success=False,
                        details="Forbidden"
                    )
                elif resp.status == 503:
                    logging.info(f"{domain_name:20} | HTTP  | Unreachable")
                    return HttpCheckResult(
                        success=False,
                        details="Unreachable"
                    )
                elif resp.status == 404:
                    logging.info(f"{domain_name:20} | HTTP  | OK (404)")
                    return HttpCheckResult(
                        success=True,
                        details="OK (404)"
                    )
                elif resp.status == 400:
                    logging.info(f"{domain_name:20} | HTTP  | OK (400)")
                    return HttpCheckResult(
                        success=True,
                        details="OK (400)"
                    )
                elif resp.status == 520:
                    logging.info(f"{domain_name:20} | HTTP  | OK (520)")
                    return HttpCheckResult(
                        success=True,
                        details="OK (520)"
                    )
                else:
                    logging.info(f"{domain_name:20} | HTTP  | {resp.status}")
                    return HttpCheckResult(
                        success=False,
                        details=str(resp.status)
                    )

    except socket.gaierror:
        logging.info(f"{domain_name:20} | HTTP  | Failed DNS resolution")
        return HttpCheckResult(
            success=False,
            details="Failed DNS resolution"
        )
    except TimeoutError:
        logging.info(f"{domain_name:20} | HTTP  | Timeout")
        return HttpCheckResult(
            success=False,
            details="Timeout"
        )
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise
