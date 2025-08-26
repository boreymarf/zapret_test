from src.https import check_https
from src.http import check_http
from src.zapret import check_zapret
from src.domains import domains
from src.quic import check_quic
from src.dns import check_dns

import asyncio
import click


@click.command()
@click.option('-a', '--append',
              multiple=True,
              help='Additional domains to check')
@click.option('-r', '--replace',
              help='Replace the default domain list')
@click.option('-t', '--throughput',
              default=3,
              help='Maximum number of simultaneous checks')
@click.option('--no-report',
              is_flag=True,
              help='Do not show report at the end of checks')
@click.option('--no-log',
              is_flag=True,
              help='Do not show check progress')
def main(append, replace, throughput, no_report, no_log):
    """Check domain availability via HTTP, HTTPS and QUIC"""
    asyncio.run(run_checks(
        append, replace, throughput, no_report, no_log
    ))


async def run_checks(append, replace, throughput, no_report, no_log):

    if check_zapret():
        print("Zapret is active!")
    else:
        print("Zapret is not active!")

    dns_provider = check_dns()
    if dns_provider is not None:
        print(f"You are using {dns_provider} provider")
    else:
        print("You are using default provider, that can spoof https certificates!")

    print('---')

    semaphore = asyncio.Semaphore(throughput)

    async def with_semaphore(func, *args, **kwargs):
        async with semaphore:
            return await func(*args, **kwargs)

    check_functions = [check_http, check_https, check_quic]

    for check_func in check_functions:
        tasks = []

        task = asyncio.sleep(2)
        tasks.append(task)

        for domain in domains:
            task = asyncio.create_task(with_semaphore(check_func, domain))
            tasks.append(task)

        await asyncio.gather(*tasks)

if __name__ == "__main__":
    main()
