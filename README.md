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

## Note


1. Website https://www.cialdnb.com/pt-br/ does not have an image from example
https://www.cialdnb.com/wp-content/uploads/2020/01/logo-cialdnb-color.png .

   Now, logo on the website is in the SVG format which does not have an actual URL.
Inline SVGs are not linked to URL. Instead, they are embedded directly in the HTML document.
I implemented a method to scrape such SVG images due to this website and saved an image in root directory which
can be opened in the browser.



   
2. https://petrobras.com.br/en/contact-us/ returned 404 as they probably had some kind of rebranding,
   link navigates to page on which is written "Conteúdo indisponível"
   I also tried with some other links to make sure script works as expected, such as :
   https://www.b2match.com/about,
   https://digacon-software.com/en/contact,
   https://gnkdinamo.hr/

