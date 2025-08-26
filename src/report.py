def print_report(results) -> None:

    total = {
        "http": 0,
        "https": 0,
        "quic": 0,
    }

    successes = {
        "http": 0,
        "https": 0,
        "quic": 0,
    }

    for result in results.values():
        for protocol in ['http', 'https']:
            total[protocol] += 1
            if result[protocol].success:
                successes[protocol] += 1
        
        if result['quic'] is not None:
            total['quic'] += 1
            if result['quic'].success:
                successes['quic'] += 1

    print("|---------------------------------------------------------------------|")
    print("|                              Report                                 |")
    print("|---------------------------------------------------------------------|")
    print("| Domain                    | HTTP        | HTTPS       | QUIC        |")
    print("|---------------------------|-------------|-------------|-------------|")
    for domain, result in results.items():
        http = "OK" if result['http'].success else "Fail"
        https = "OK" if result['https'].success else "Fail"
        quic = "Skipped" if result['quic'] is None else "OK" if result['quic'].success else "Fail"

        print(f"| {domain:25} | {http:11} | {https:11} | {quic:11} |")
    print("|---------------------------|-------------|-------------|-------------|")

    http_percent = successes['http'] / total['http'] * 100 if total['http'] > 0 else 0
    https_percent = successes['https'] / total['https'] * 100 if total['https'] > 0 else 0
    quic_percent = successes['quic'] / total['quic'] * 100 if total['quic'] > 0 else 0

    http_str = f"{successes['http']}/{total['http']} ({http_percent:.0f}%)"
    https_str = f"{successes['https']}/{total['https']} ({https_percent:.0f}%)"
    quic_str = f"{successes['quic']}/{total['quic']} ({quic_percent:.0f}%)"

    print(f"| Total:                    | {http_str:11} | {https_str:11} | {quic_str:11} |")
