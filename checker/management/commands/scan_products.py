import asyncio
import time
import os

from django.core.management.base import BaseCommand

from checker.models import Product
from checker.parser import start_parser


os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

class Command(BaseCommand):
    help = 'Scanning all products'

    def handle(self, *args, **options):
        result = {}
        products = Product.objects.all().values_list('url')
        urls = [product[0] for product in products]

        start = time.time()
        asyncio.run(start_parser(urls, result))
        print('Time: {}'.format(time.time() - start))
        