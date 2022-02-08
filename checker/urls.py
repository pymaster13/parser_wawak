from django.urls import path

from .views import (AnalysisPrice, AnalysisStock, CheckProduct,
                    CheckProducts, HistoryProduct)


urlpatterns = [
    path('product/history/', HistoryProduct.as_view(), name='history_product'), 
    path('products/', CheckProducts.as_view(), name='check_products'),
    path('product/', CheckProduct.as_view(), name='check_product'),
    path('analysis/price/', AnalysisPrice.as_view(), name='analysis_prices'),
    path('analysis/stock/', AnalysisStock.as_view(), name='analysis_stock'),
]