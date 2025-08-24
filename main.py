from src.https import check_https
from src.http import check_http
from src.icmp import check_icmp
from src.zapret import check_zapret

def main():
    print(check_zapret())
    print(check_icmp('example.com'))
    print(check_http('example.com'))
    print(check_https('example.com'))


if __name__ == "__main__":
    main()
