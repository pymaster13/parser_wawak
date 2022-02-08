# Parser for wawak.com

This project is a backend for online parsing for site https://wawak.com (2022). 

## Getting Started
Python version: 3.9.10

Clone project:
```
git clone https://github.com/pymaster13/parser_wawak.git && cd parser_wawak
```

Create and activate virtual environment:
```
python3 -m venv venv && source venv/bin/activate
```

Install libraries:
```
python3 -m pip install -r requirements.txt
```

Run local Django server:
```
python3 manage.py runserver --noreload --nothreading
```

## Functional

- Add goods/goods (links) to the database and scanning for availability and price changes, and immediately give the result of the scan in response.
- Get history for a specific product.
- Get a list of products that have changed their price or "stock" status.
- Get a list of products that have changed their "stock" status.
- Once a day, scan all products from the database for changes. 

### Features

Main libraries that are used : 
* Django 4,
* djangorestframework,
* aiohttp (for asynchronous requests),
* beautifulsoup4, lxml (for parsing html),
* drf-spectacular (for showing API schema),
* pyppeteer (for loading web-pages in chromium).

A feature of the "wawak.com site" is that almost all data is generated using ajax requests that cannot be intercepted using requests.get().
In this regard, it was decided to parse the data, send a specific ajax request for each product.

To speed up and optimize requests, the "aiohttp" asynchronous library was used.

However, there is also a problem that for some products (there are quite a few of them) it was not possible to track and select the type of ajax request.

Therefore, for such goods, the "light" asynchronous pyppeteer library works in asynchronous mode (similar in meaning to work on selenium). Compared to the synchronous version, the acceleration was 2.5 times. 
