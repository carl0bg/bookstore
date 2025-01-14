
# app_name = 'products'

# urlpatterns = [
#     path('', Products.as_view(), name = 'index'),
#     path('category/<int:category_id>', Products.as_view(), name = 'category'),
#     path('page/<int:page_number>', Products.as_view(), name = 'paginator'),

#     path('baskets/add/<int:product_id>/', basket_add, name = 'basket_add'),
#     path('baskets/remove/<int:basket_id>/', basket_remove, name = 'basket_remove'),
# ]
from django.urls import path

from products.views import Products, basket_add, basket_remove

app_name = 'products'

urlpatterns = [
    path('', Products.as_view(), name='index'),
    path('category/<int:category_id>/', Products.as_view(), name='category'),
    path('page/<int:page>/', Products.as_view(), name='paginator'),

    path('baskets/add/<int:product_id>/', basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
]