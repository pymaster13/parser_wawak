from math import prod
from django.db import models


class Product(models.Model):
    url = models.URLField(max_length=100, verbose_name='URL', unique=True)
    datetime_add = models.DateTimeField(
                                    auto_now_add=True,
                                    blank=True,
                                    verbose_name='Дата добавления'
                                    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.url


class ProductInfo(models.Model):
    product = models.ForeignKey(
                                Product,
                                on_delete=models.CASCADE,
                                related_name='product',
                                verbose_name='Продукт'
                                )
    name = models.CharField(max_length=100, verbose_name='Название')
    price = models.FloatField(verbose_name='Цена')
    stock = models.BooleanField(verbose_name='Наличие')
    datetime_scan = models.DateTimeField(auto_now_add=True, blank=True,
            verbose_name='Дата сканирования')

    class Meta:
        verbose_name = 'Информация о товаре'
        verbose_name_plural = 'Информация о товарах'

    @classmethod
    def get_history(cls, product):
        history = cls.objects.filter(
                                    product=product
                                    ).order_by('-datetime_scan')
        if history:
            return [record.history_view for record in history]
        else:
            return f'History {product.link} is blank.'

    @staticmethod
    def get_changed_products(*, type):
        chg = {}
        for product in Product.objects.all():
            history = ProductInfo.objects.filter(
                                                product=product
                                                ).order_by('-datetime_scan')
            if len(history) > 1:
                if getattr(history[0],type) != getattr(history[1],type):
                    chg[product.url] = 'now - {}, old - {}, changed {}'.format(
                                                    getattr(history[0],type),
                                                    getattr(history[1],type),
                                                    history[0].datetime_scan
                                                    )
        return chg

    @property
    def history_view(self):
        return {'price': self.price,
                'stock': self.stock,
                'scanned': self.datetime_scan}

    def __str__(self):
        return self.product.url
