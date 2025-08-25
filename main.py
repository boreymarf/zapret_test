from src.https import check_https
from src.http import check_http
from src.zapret import check_zapret
from src.domains import domains
from src.quic import check_quic

import asyncio


def main():

    if check_zapret():
        print("Zapret is active!")
    else:
        print("Zapret is not active!\n")

    for domain in domains:

        # print(check_icmp(domain))
        # print(check_http(domain))
        print(domain)
        # print(f"HTTP: {check_http(domain)}")
        # print(f"HTTPS: {check_https(domain)}")
        asyncio.run(check_quic(domain))
        print("")


if __name__ == "__main__":
    main()
