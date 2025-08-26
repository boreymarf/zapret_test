from src.report import print_report
from src.https import check_https
from src.http import check_http
from src.zapret import check_zapret
from src.domains import DEFAULT_DOMAINS, read_domains_from_file
from src.quic import check_quic
from src.dns import check_dns

import logging
import asyncio
import click

from pprint import pprint


@click.command()
@click.option('-a', '--append',
              multiple=True,
              help='Path to file with additional domains to check (one per line)')
@click.option('-r', '--replace',
              help='Path to file to replace the default domain list (one per line)')
@click.option('-t', '--throughput',
              default=3,
              help='Maximum number of simultaneous checks')
@click.option('--no-report',
              is_flag=True,
              help='Do not show report at the end of checks')
@click.option('--log-level', 
              type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], case_sensitive=False),
              default='INFO',
              help='Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)')
def main(append, replace, throughput, no_report, log_level):
    """Check domain availability via HTTP, HTTPS and QUIC"""
    asyncio.run(run_checks(
        append, replace, throughput, no_report, log_level
    ))


async def run_checks(append, replace, throughput, no_report, log_level):

    level = getattr(logging, log_level.upper())
    logging.basicConfig(level=level, format='%(message)s')
    logging.getLogger('quic').setLevel(logging.WARNING)
    logging.getLogger('asyncio').setLevel(logging.WARNING)

    if replace:
        domains = read_domains_from_file(replace)
    else:
        domains = DEFAULT_DOMAINS

    for append_file in append:
        additional_domains = read_domains_from_file(append_file)
        domains.extend(additional_domains)

    # Remove duplicates
    domains = list(set(domains))

    if check_zapret():
        logging.info("Zapret is active!")
    else:
        logging.info("Zapret is not active!")

    dns_provider = check_dns()
    if dns_provider is not None:
        logging.info(f"You are using {dns_provider} provider")
    else:
        logging.info("You are using default provider, that can spoof https certificates!")

    semaphore = asyncio.Semaphore(throughput)

    async def with_semaphore(func, *args, **kwargs):
        async with semaphore:
            return await func(*args, **kwargs)

    results = {}

    # HTTP
    tasks = []
    for domain in domains:
        task = asyncio.create_task(with_semaphore(check_http, domain))
        tasks.append(task)

    http_results = await asyncio.gather(*tasks)
    for domain, result in zip(domains, http_results):
        if domain not in results:
            results[domain] = {}
        results[domain]['http'] = result

    # HTTPS
    tasks = []
    for domain in domains:
        task = asyncio.create_task(with_semaphore(check_https, domain))
        tasks.append(task)

    https_results = await asyncio.gather(*tasks)
    for domain, result in zip(domains, https_results):
        if domain not in results:
            results[domain] = {}
        results[domain]['https'] = result

    # QUIC
    tasks = []
    for domain in domains:
        https_result = results[domain]['https']

        skip_quic = (
            https_result is not None 
            and https_result.supports_quic is not None 
            and https_result.supports_quic == False
        )
        
        if not skip_quic:
            task = asyncio.create_task(with_semaphore(check_quic, domain))
            tasks.append((domain, task))
        else:
            logging.debug(f"{domain} is set to NONE")
            if domain not in results:
                results[domain] = {}
            results[domain]['quic'] = None

    for domain, task in tasks:
        if domain not in results:
            results[domain] = {}
        results[domain]['quic'] = await task
    
    if not no_report:
        print("\n")
        print_report(results)

if __name__ == "__main__":
    main()
