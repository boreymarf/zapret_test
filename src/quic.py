from aioquic.quic.configuration import QuicConfiguration
from aioquic.asyncio.client import connect
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.events import ConnectionTerminated

ERROR_CODES = {
    0: "NO_ERROR",
    1: "TIMEOUT",
    296: "INSTANT_FAIL"
}

code = 0


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


async def check_quic(hostname: str):
    configuration = QuicConfiguration(
        alpn_protocols=["h3"],
        idle_timeout=2)

    try:
        async with connect(
            hostname,
            443,
            configuration=configuration,
            create_protocol=DummyProtocol
        ):
            print(f"{hostname:20} | QUIC  | OK")
            return True

    except ConnectionError:
        if code == 1:
            print(f"{hostname:20} | QUIC  | Timeout")
        elif code == 296:
            print(f"{hostname:20} | QUIC  | Instant fail")
        else:
            print(f"{hostname:20} | QUIC  | {code}")

    except Exception as e:
        print(f"Unexpected error happened! {e}")
        raise

    # finally:
    #     print(ERROR_CODES.get(code))
