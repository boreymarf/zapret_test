from src.blocked_patters import is_blocked_hostname

from aiohttp import ClientSession, ClientTimeout, ClientConnectorError
from aiohttp.client_exceptions import ClientConnectorCertificateError
from aiohttp import TCPConnector
from dataclasses import dataclass

import ssl
import certifi
import socket
import asyncio
import logging


# Use up to date certificates and not default ones
ssl_context = ssl.create_default_context(cafile=certifi.where())


@dataclass
class HttpsCheckResult:
    success: bool
    details: str | None
    supports_quic: bool | None


async def check_https(domain_name) -> HttpsCheckResult:
    host_name = None

    try:

        ip_address = await asyncio.to_thread(socket.gethostbyname, domain_name)

        try:
            host_name = await asyncio.to_thread(socket.gethostbyaddr, ip_address)
            host_name = host_name[0]
        except (socket.herror, socket.gaierror):
            pass

        async with ClientSession(
            timeout=ClientTimeout(2),
            max_line_size=16380,
            max_field_size=16380,
            connector=TCPConnector(ssl=ssl_context)
        ) as session:
            async with session.get(f"https://{domain_name}") as resp:

                result = HttpsCheckResult(
                    success=False, details=None, supports_quic=None)

                # Check HTTP/3 support
                alt_svc_header = resp.headers.get('Alt-Svc')
                if alt_svc_header and 'h3' in alt_svc_header:
                    logging.debug(f"{domain_name:20} | HTTP/3 (QUIC) | Supported")
                    result.supports_quic = True
                else:
                    logging.debug(f"{domain_name:20} | HTTP/3 (QUIC) | Not Supported")
                    result.supports_quic = False

                if resp.status == 200:
                    logging.info(f"{domain_name:20} | HTTPS | OK")
                    result.success = True
                    return result
                elif resp.status == 503:
                    logging.info(f"{domain_name:20} | HTTPS | Unreachable")
                    result.success = False
                    result.details = "Unreachable"
                    return result
                else:
                    logging.info(f"{domain_name:20} | HTTPS | {resp.status}")
                    result.success = False
                    result.details = str(resp.status)
                    return result

    except socket.gaierror:
        logging.info(f"{domain_name:20} | HTTP  | Failed DNS resolution")
        return HttpsCheckResult(
            success=False,
            details="Failed DNS resolution",
            supports_quic=None
        )
    except TimeoutError:
        logging.info(f"{domain_name:20} | HTTPS | Timeout")
        return HttpsCheckResult(
            success=False,
            details="Timeout",
            supports_quic=None
        )
    except ClientConnectorCertificateError:
        logging.info(f"{domain_name:20} | HTTPS | Bad certificate")
        return HttpsCheckResult(
            success=False,
            details="Fake certificate",
            supports_quic=None
        )
    except ClientConnectorError as e:
        if is_blocked_hostname(host_name):
            logging.info(f"{domain_name:20} | HTTPS | Blocked")
            return HttpsCheckResult(
                success=False,
                details="Blocked",
                supports_quic=None
            )
        logging.info(f"{domain_name:20} | HTTPS | Connection error: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise
