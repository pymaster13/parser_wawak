import asyncio
from json import loads
import time

import aiohttp
from asgiref.sync import sync_to_async
from bs4 import BeautifulSoup
from pyppeteer import launch

# from test_data import LINKS
from .models import Product, ProductInfo


def _create_product_info(**kwargs):
    """
    Function for async product creation 
    """
    return ProductInfo.objects.create(**kwargs)


def parse_html(soup):
    """
    Function for parsing HTML-code
    """
    name = soup.find('h1', class_='product-name data-hj-whitelist').text
    price = soup.find('span', class_='price').text[1:]
    div = soup.find('div', id='pdp')

    product_code = div['data-product-code']
    selected_fiels = loads(div['data-preselected-filters'])

    return name, price, product_code, selected_fiels


async def go_to_link(session, link, result, not_response):
    """
    Async function for to go to site 
    by input link and to parse HTML-code
    via aiohttp
    """
    async with session.get(link) as response:  
        html = await response.text()
        url = link.split('?sku')[0]

        soup = BeautifulSoup(html, 'lxml')

        name, price, product_code, selected_fiels = parse_html(soup)
        result[link] = {}
        result[link]['product'], _ = await sync_to_async(
                                        Product.objects.get_or_create,
                                        thread_sensitive=True
                                        )(url=link)
        result[link]['name'] = name
        result[link]['price'] = price

        ajax_link = f'{url}/SelectVariant/?productCode={product_code}'

        for_target_ajax = {}
        if selected_fiels:
            for item in selected_fiels:
                for_target_ajax[item['Name']] = item['Facet']

        if for_target_ajax:
            for key in for_target_ajax:
                ajax_link += f'&{key}={for_target_ajax[key]}'

        async with session.get(ajax_link) as response_ajax:
            
            assert response_ajax.status == 200, 'NOT 200 RESPONSE STATUS'

            payload = await response_ajax.json()
            if payload['Variant']:
                result[link]['stock'] = payload['Variant']['IsInStock']
            else:
                not_response.append(link)


async def go_to_link_by_browser(browser, link, result):
    """
    Async function for to go to site 
    by input link and to parse HTML-code
    via chromium
    """
    page = await browser.newPage()
    await page.goto(link)
    page_content = await page.content()
    
    soup = BeautifulSoup(page_content, 'lxml')
    
    stock = bool(soup.find('div', class_='stock-notification in-stock'))
    result[link]['stock'] = stock


async def start_parser(links, result, one_link=False):
    """
    Main async function for create tasks for event loop 
    """
    not_response = []
    async with aiohttp.ClientSession() as session:
        if one_link:
            links = [links]
        
        tasks = [asyncio.create_task(go_to_link(
                                    session,
                                    link,
                                    result,
                                    not_response
                                    )) for link in links] 

        await asyncio.gather(*tasks)

    if not_response:
        browser = await launch(headless=True, autoClose=False)
        tasks = [asyncio.create_task(go_to_link_by_browser(
                                    browser,
                                    link,
                                    result
                                    )) for link in not_response]
        await asyncio.gather(*tasks)
        await browser.close()

    for link, items in result.items():
        await sync_to_async(
                            _create_product_info,
                            thread_sensitive=True
                            )(**items)

    for item, value in result.items():
        del value['product']

    print(f'Result:\n{result}\n\n')    
    print(f'Not response: {not_response}\n')


if __name__ == '__main__':
    """
    Function for testing of module
    """
    start = time.time()
    asyncio.run(start_parser(), debug=False)
    print('Time: {}'.format(time.time() - start))
