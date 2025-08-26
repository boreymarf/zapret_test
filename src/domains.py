import logging

DEFAULT_DOMAINS = [
    "vk.com",
    "google.com",
    "youtube.com",
    "rutracker.org",
    "x.com",
    "facebook.com",
    "torproject.org",
    "tails.net",
    "discord.com",
    "cloudflare-ech.com"
]


def read_domains_from_file(file_path):
    """Read domains from file, one per line"""
    try:
        with open(file_path, 'r') as f:
            domains = [line.strip() for line in f if line.strip()]
            return domains
    except FileNotFoundError:
        logging.info(f"Error: File {file_path} not found")
        return []
    except Exception as e:
        logging.info(f"Error reading file {file_path}: {e}")
        return []
