import asyncio
from aioquic.quic.configuration import QuicConfiguration
from aioquic.asyncio.client import connect
from aioquic.asyncio.protocol import QuicConnectionProtocol


class DummyProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._closed = asyncio.Event()

    def connection_made(self, transport):
        super().connection_made(transport)

    def quic_event_received(self, event):
        pass

    def connection_lost(self, exc):
        super().connection_lost(exc)
        self._closed.set()

    async def wait_closed(self):
        await self._closed.wait()


async def check_quic(hostname: str):
    configuration = QuicConfiguration(alpn_protocols=["h3"])
    background_errors = []

    # Simple exception handler that just captures errors
    def exception_handler(loop, context):
        error_msg = context.get("message", "Unknown error")
        exception = context.get("exception")

        if exception:
            error_details = f"{type(exception).__name__}: {str(exception)}"
        else:
            error_details = error_msg

        background_errors.append(error_details)

    # Set the exception handler
    loop = asyncio.get_event_loop()
    original_handler = loop.get_exception_handler()
    loop.set_exception_handler(exception_handler)

    try:
        async with asyncio.timeout(2):
            async with connect(
                hostname,
                443,
                configuration=configuration,
                create_protocol=DummyProtocol
            ) as protocol:
                print(f"QUIC connection to {hostname} successful!")
                return True

    except asyncio.TimeoutError:
        print(f"QUIC connection to {hostname} timed out")
        if background_errors:
            print(f"Background errors: {background_errors}")
        return False

    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e) or "No error message"
        print(f"QUIC connection to {hostname} failed: {
              error_type}: {error_msg}")

        if background_errors:
            print(f"Background errors: {background_errors}")
        return False

    finally:
        # Always restore the original handler
        loop.set_exception_handler(original_handler)
