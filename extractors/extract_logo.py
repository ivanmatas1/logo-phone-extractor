import os
import re
from urllib.parse import urljoin, quote
from bs4 import BeautifulSoup
from typing import Optional
from constants.constants import LOGO, URL_PATTERN
from utils.utils import get_domain_name


def extract_logo_url(url: str, html: str) -> Optional[str]:
    """
    Retrieves the URL of a website's logo.
    It checks image tags, anchor tags, svg embedded in html and falls back to 'simple logo' search in img tags
    """
    soup = BeautifulSoup(html, 'html.parser')
    domain_name = get_domain_name(url)

    logo_extractors = [
        lambda: find_logo_in_img_tags(soup, domain_name),
        lambda: find_svg_logo(soup),
        lambda: find_logo_in_anchor_tags(soup, domain_name, url),
        lambda: find_logo_fallback(soup)
    ]

    for extractor in logo_extractors:
        logo_url = extractor()
        if logo_url:
            return urljoin(url, quote(logo_url))

    return None


def find_logo_in_img_tags(soup: BeautifulSoup, domain_name: str) -> Optional[str]:
    """
    Searches through all the image tags on the page.
    Extracts the image name from the 'src' attribute and looks for images that have both
    'logo' and the website's domain name in their name.
    We extract image name without extension https://www.example.com/images/company-logo.png -> company-logo
    """
    for img_element in soup.find_all('img', {'src': True}):
        src = img_element.get('src')
        image_name = src.split('/')[-1].split('.')[0]
        if LOGO in image_name and domain_name in image_name:
            return img_element.get('src')

    return None


def find_svg_logo(soup: BeautifulSoup) -> None:
    """
    Extracts an inline SVG element from the HTML content.
    Only SVGs whose parent element class contains the word 'logo' to filter potential logo's.
    Save the SVG content to a file in the root directory.
    """
    svg_elements = soup.find_all('svg', {'xmlns': 'http://www.w3.org/2000/svg'})

    for svg_element in svg_elements:
        parent = svg_element.find_parent()

        if parent and parent.has_attr('class'):
            parent_classes = " ".join(parent['class']).lower()
            if LOGO in parent_classes:
                svg_content = str(svg_element)
                file_path = os.path.join(os.getcwd(), 'extracted_logo.svg')

                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(svg_content)
                print("Embedded SVG inline element saved in root directory")
                return None

    return None


def find_logo_in_anchor_tags(soup: BeautifulSoup, domain_name: str, page_url: str) -> Optional[str]:
    """
    Searches through all anchor tags on the page for self-referential links containing images.
    If href is ('/') - root or if url and href url are equal or domain name is in href url, we extract url from img src
    attribute.

    - If an anchor tag links to '/' and it contains an image, that image is likely to be the website's logo.
    """
    stripped_url = page_url.strip('/')
    normalized_url = re.sub(URL_PATTERN, '', stripped_url)
    url = normalized_url if normalized_url != stripped_url else None

    for a in soup.find_all('a', href=True):
        href_url = a.get('href').strip('/')
        normalized_href = re.sub(URL_PATTERN, '', href_url)
        href = normalized_href if normalized_href != href_url else None

        if href is not None and url is not None:
            if href == url or href == '/' or domain_name in href:
                img = a.find('img', {'src': True})
                if img:
                    return img.get('src')

    return None


def find_logo_fallback(soup: BeautifulSoup) -> Optional[str]:
    """
    This function iterates through all <img> tags on the page and checks if the word 'logo'
    appears anywhere in the element
    """
    for img_element in soup.find_all('img', {'src': True}):
        if LOGO in str(img_element).lower():
            return img_element.get('src')

    return None
