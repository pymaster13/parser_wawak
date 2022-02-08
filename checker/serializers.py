import ast

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    url = serializers.CharField(
                                required=True,
                                validators=[URLValidator(schemes=['https'])],
                                )

    class Meta:
        model = Product
        fields = ('url', )

        
class ProductsSerializer(serializers.Serializer):
    urls = serializers.ListField(child = serializers.CharField())

    def validate_urls(self, urls):
        validate = URLValidator(schemes=['https'])

        for list in urls:
            list = ast.literal_eval(list)
            for url in list:
                try:
                    validate(url)
                except ValidationError as e:
                    print(f'Exception: {e}')
        return list
