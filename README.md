# Logo and phone number extractor

This is a web scraper that extracts logos and phone numbers from websites using
BeautifulSoup library.

It takes a website URL as an input and outputs both the logo URL
and any found phone numbers, making it useful
for gathering basic contact and branding information from websites automatically.

## Key features

- Logo extraction from web pages and returning logo URL
- Phone numbers detection: fetch all phone numbers from a given website URL

## Getting Started

### Installation

Clone the repository:

##### git clone <repository-url>

Navigate to project directory:

##### cd logo-phone-extractor

Create a virtual environment:

##### python -m venv venv

Activate the virtual environment:

##### On Windows -> venv\Scripts\activate

##### On Linux/macOS -> source venv/bin/activate

Install required packages:

##### pip install -r requirements.txt

### Usage

Run the extractor by providing a URL:

##### python extract.py {URL}
