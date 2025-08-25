from src.https import check_https
from src.http import check_http
from src.zapret import check_zapret
from src.domains import domains
from src.quic import check_quic

import asyncio
import socket


async def main():

    if check_zapret():
        print("Zapret is active!")
    else:
        print("Zapret is not active!\n")

    semaphore = asyncio.Semaphore(10)

    tasks = []
    for domain in domains:
        async with semaphore:
            task = asyncio.create_task(check_http(domain))
            tasks.append(task)

    await asyncio.gather(*tasks)

    tasks = []
    for domain in domains:
        async with semaphore:
            task = asyncio.create_task(check_https(domain))
            tasks.append(task)

    await asyncio.gather(*tasks)

    tasks = []
    for domain in domains:
        async with semaphore:
            task = asyncio.create_task(check_quic(domain))
            tasks.append(task)

    await asyncio.gather(*tasks)

if __name__ == "__main__":

    print(socket.gethostbyaddr("188.186.146.207"))

    asyncio.run(main())
