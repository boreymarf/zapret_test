from aiohttp import ClientSession, ClientTimeout


async def check_http(domainname):
    try:
        async with ClientSession(
            timeout=ClientTimeout(2),
            max_line_size=16380,
            max_field_size=16380
        ) as session:
            async with session.get(f"http://{domainname}") as resp:
                if resp.status == 200:
                    print(f"{domainname:20} | HTTP  | OK")
                elif resp.status == 503:
                    print(f"{domainname:20} | HTTP  | Unreachable")
                else:
                    print(f"{domainname:20} | HTTP  | {resp.status}")
    except TimeoutError:
        print(f"{domainname:20} | HTTP  | Timeout")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise
