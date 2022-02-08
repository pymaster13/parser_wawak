import asyncio
import time

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Product, ProductInfo
from .serializers import ProductSerializer, ProductsSerializer
from .parser import start_parser


class CheckProduct(APIView):
    """
    API endpoint for check one product
    """
    serializer_class = ProductSerializer
    
    def post(self, request):
        product_serializer = ProductSerializer(data=request.data)
        
        if product_serializer.is_valid(raise_exception=True): 
            result = {}
            url = product_serializer.validated_data['url']

            start = time.time()
            asyncio.run(start_parser(
                                    url,
                                    result,
                                    one_link=True
                                    ))
            print('Time: {}'.format(time.time() - start))

            return Response(result)
        else:
            return Response("Product is checked unsuccessfully")


class CheckProducts(APIView):
    """
    API endpoint for check many products
    """
    serializer_class = ProductsSerializer
    
    def post(self, request):
        products_serializer = ProductsSerializer(data=request.data)

        if products_serializer.is_valid(raise_exception=True): 
            result = {}
            urls = products_serializer.validated_data['urls']
            
            start = time.time()
            asyncio.run(start_parser(urls, result))
            print('Time: {}'.format(time.time() - start))

            return Response(result)
        else:
            return Response("Products are checked unsuccessfully")


class HistoryProduct(APIView):
    """
    API endpoint to show product history 
    """
    def get(self, request):
        product_serializer = ProductSerializer(data=request.query_params)
        if product_serializer.is_valid(raise_exception=True): 
            url = product_serializer.validated_data['url']
            
            try:
                product = Product.objects.get(url=url)
            except ObjectDoesNotExist:
                return Response(f"Product {url} doesn't exist in database")
            
            history = ProductInfo.get_history(product)
            return Response(history)
        else:
            return Response("Input correct url!")
      

class AnalysisPrice(APIView):
    """
    API endpoint for analysis of all products prices changes 
    """
    def get(self, request):
        return Response(ProductInfo.get_changed_products(type='price'))

class AnalysisStock(APIView):
    """
    API endpoint for analysis of all products stock changes 
    """
    def get(self, request):
        return Response(ProductInfo.get_changed_products(type='stock'))
