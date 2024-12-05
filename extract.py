import sys

import validators
from extractors.extract_logo import extract_logo_url
from extractors.extract_phone_numbers import extract_phone_numbers
from utils.utils import fetch_page


def main():
    if len(sys.argv) != 2:
        print("Invalid number of input parameters, correct command is: python extract.py <URL>", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    if not validators.url(url):
        print("Invalid URL format.", file=sys.stderr)
        sys.exit(1)

    html = fetch_page(url)
    if not html:
        print("Failed to fetch the page content.", file=sys.stderr)
        sys.exit(1)

    phone_numbers = extract_phone_numbers(html)
    if phone_numbers:
        print(phone_numbers)
    else:
        print("None", file=sys.stderr)

    logo_url = extract_logo_url(url, html)
    if logo_url:
        print(logo_url)
    else:
        print("None", file=sys.stderr)


if __name__ == "__main__":
    main()
