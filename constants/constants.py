from typing import Set, Pattern
import re

# Logo extraction constants
LOGO = 'logo'
URL_PATTERN = r'^https?://(?:www\.)?'

# Phone number constants
PHONE_REGEX: Pattern = re.compile(
    r'(?:(?:\+|00)?\d{1,3})?[\s.-]?\(?\d{1,4}\)?[\s.-]?\d{1,4}[\s.-]?\d{1,4}[\s.-]?\d{1,4}(?:[\s.-]?\d{1,5})?')

CONTEXT_KEYWORDS: Set[str] = {
    'phone', 'tel', 'mobile', 'cell', 'contact', 'fax', 'number', 'dial', 'call', 'talk', 'INFOTELEFON'
}

CONTEXT_RANGE: int = 100
MIN_PHONE_LENGTH: int = 6
MAX_PHONE_LENGTH: int = 15
