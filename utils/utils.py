import random
import sys
import time
from typing import Optional
from urllib.parse import urlparse

import requests

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/53.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.1.2 '
    'Safari/602.3.12',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 '
    'Mobile/14E304 Safari/602.1 '
]


# def fetch_page(url: str) -> Optional[str]:
#     """Fetch the HTML content of the page."""
#     headers = {'User-Agent': random.choice(USER_AGENTS)}
#     try:
#         response = requests.get(url, headers=headers, timeout=10)
#         response.raise_for_status()
#         return response.text
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching the URL: {e}", file=sys.stderr)
#         return None


def fetch_page(url: str) -> Optional[str]:
    """Fetch the HTML content of the page."""
    session = requests.Session()
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive'
    }

    retries = 5
    delay = 2
    for attempt in range(retries):
        try:
            response = session.get(url, headers=headers, timeout=10)

            if response.status_code == 403:
                print("403 Forbidden, retrying..")
                time.sleep(delay + random.uniform(1, 3))
                delay *= 2
                continue
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the URL: {e}", file=sys.stderr)
            return None
    print(f"Failed to fetch the URL after {retries} attempts.")
    return None


def get_domain_name(url: str) -> str:
    """Extract the domain name from a URL."""
    parsed_url = urlparse(url)
    domain_name = parsed_url.netloc
    if domain_name.startswith('www.'):
        domain_name = domain_name[4:]
    return domain_name.split(".")[0]
