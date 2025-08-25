from aioquic.quic.configuration import QuicConfiguration
from aioquic.asyncio.client import connect
from aioquic.asyncio.protocol import QuicConnectionProtocol


class DummyProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def quic_event_received(self, event):
        pass


async def check_quic(hostname: str):
    configuration = QuicConfiguration(
        alpn_protocols=["h3"],
        idle_timeout=5)

    try:
        async with connect(
            hostname,
            443,
            configuration=configuration,
            create_protocol=DummyProtocol
        ):
            print(f"QUIC connection to {hostname} successful!")
            return True

    except ConnectionError:
        print(f"Failed to connect to {hostname}")

    except Exception as e:
        print(f"Unexpected error happened! {e}")
        raise
