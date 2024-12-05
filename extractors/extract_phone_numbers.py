import re
from typing import Iterator, List, Optional
from bs4 import BeautifulSoup
from constants.constants import CONTEXT_RANGE, CONTEXT_KEYWORDS, MIN_PHONE_LENGTH, MAX_PHONE_LENGTH, PHONE_REGEX


def extract_phone_numbers(html_content: str) -> Optional[str]:
    """
    Main function to extract and validate phone numbers from a webpage.
    Processes both raw text content and specific HTML elements to find phone numbers,
    validate them, and check surrounding context for a match.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    text_content = soup.get_text()

    text_matches = extract_numbers_from_text(text_content)
    element_matches = extract_numbers_from_elements(soup)

    validated_numbers = set()

    for match in list(text_matches) + element_matches:
        number = match.group().strip()
        if is_valid_number(number) and check_context(text_content, text_content.find(number),
                                                     text_content.find(number) + len(number)):
            validated_numbers.add(number)

    return ', '.join(validated_numbers) if validated_numbers else None


def extract_numbers_from_text(html_content: str) -> Iterator[re.Match]:
    """ Extracts phone numbers from text content using regex."""
    return PHONE_REGEX.finditer(html_content)


def extract_numbers_from_elements(soup: BeautifulSoup) -> List[re.Match]:
    """
    Extracts phone numbers from nested HTML elements (div, a, span),
    Searches through HTML elements, checking both their text content
    and attribute values for potential phone numbers.
    """
    numbers = []

    for tag in soup.find_all(['div', 'a', 'span']):
        text = tag.get_text()
        if text:
            matches = PHONE_REGEX.finditer(text)
            numbers.extend(matches)

        # Check for numbers stored in attributes
        for attr_value in tag.attrs.values():
            # Only process string attributes -> like href
            if isinstance(attr_value, str):
                matches = PHONE_REGEX.finditer(attr_value)
                numbers.extend(matches)

    return numbers


def is_valid_number(number: str) -> bool:
    """ Check if a number is valid by checking its length."""
    if '.' in number:
        return False

    validated_number = re.sub(r'[^\d()+]', '', number)

    if len(validated_number) < MIN_PHONE_LENGTH or len(validated_number) > MAX_PHONE_LENGTH:
        return False

    return True


def check_context(html_content: str, start_index: int, end_index: int) -> bool:
    """ Check text before and after a potential phone number to find phone-related keywords."""
    start = max(0, start_index - CONTEXT_RANGE)
    end = min(len(html_content), end_index + CONTEXT_RANGE)
    context = html_content[start:end].lower()

    return any(keyword in context for keyword in CONTEXT_KEYWORDS)
