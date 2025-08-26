from aioquic.quic.configuration import QuicConfiguration
from aioquic.asyncio.client import connect
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.events import ConnectionTerminated
from dataclasses import dataclass

import logging
import ssl

ERROR_CODES = {
    0: "NO_ERROR",
    1: "TIMEOUT",
    296: "INSTANT_FAIL"
}

code = 0


@dataclass
class QuicCheckResult:
    success: bool
    details: str | None


class DummyProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_error_code = 0

    def quic_event_received(self, event):
        if isinstance(event, ConnectionTerminated):
            self.last_error_code = event.error_code

            # This is a temporary, until I'll figure out how to get code from
            # the Protocol class properly
            global code
            code = event.error_code


async def check_quic(domain_name: str):

    configuration = QuicConfiguration(
        alpn_protocols=["h3"],
        idle_timeout=2)

    try:
        async with connect(
            domain_name,
            443,
            configuration=configuration,
            create_protocol=DummyProtocol
        ):
            logging.info(f"{domain_name:20} | QUIC  | OK")
            return QuicCheckResult(
                success=True,
                details=None
            )

    except ssl.SSLCertVerificationError:
        logging.info(f"{domain_name:20} | QUIC  | Bad certificate")
        return QuicCheckResult(
            success=False,
            details="Bad certificate"
        )
    except ConnectionError:
        if code == 1:
            logging.info(f"{domain_name:20} | QUIC  | Timeout")
            return QuicCheckResult(
                success=False,
                details="Timeout"
            )
        elif code == 296:
            logging.info(f"{domain_name:20} | QUIC  | Instant fail")
            return QuicCheckResult(
                success=False,
                details="Instant fail"
            )
        else:
            logging.warning(f"{domain_name:20} | QUIC  | {code}")
            return QuicCheckResult(
                success=False,
                details=str(code)
            )
    except Exception as e:
        logging.error(f"Unexpected error happened! {e}")
