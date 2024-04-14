from django.db.models.query import QuerySet
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView


from common.utils import TitleMixin
from products.models import Product, ProductCategory, Basket
from users.models import User



class Index(TitleMixin, TemplateView):
    template_name = 'products/index2.html'
    title = 'Bookstore'


# def products(request, category_id=None, page_number=1): #может и не быть category id, поэтому None


#     products = Product.objects.filter(category_id = category_id) if category_id else Product.objects.all()
   
#     per_page = 3 #это сколько товаров продут показано
#     paginator = Paginator(products, per_page)
#     products_paginator = paginator.page(page_number)
    
#     context = {
#         'title':'Store - Каталог',
#         'products': products_paginator,
#         'categories': ProductCategory.objects.all(),
#     }    
#     return render(request, 'products/products.html', context)


class Products(TitleMixin, ListView): #в ListView имеется MultipleObjectMixin удобный особенно для пагинации 
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3 #позже надо будет попробовать сделать динамично
    title = 'Store - Каталог'
    
    def get_queryset(self):
        queryset = super(Products, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset
    
    def get_context_data(self, *, object_list = None, **kwargs):
        context = super(Products, self).get_context_data()
        context['categories'] = ProductCategory.objects.all()
        return context





@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id = product_id)
    baskets = Basket.objects.filter(user = request.user, product = product)
    
    if not baskets.exists():
        Basket.objects.create(user = request.user, product = product, quantity = 1)
    else:
        basket = baskets.first()
        basket.quantity+=1
        basket.save()

    # return HttpResponseRedirect(request.META['HTTP_REFERER']) #возвращает на ту же страничку где было выполнено дейсствие 
    url = request.META.get('HTTP_REFERER', '/')
    response = redirect(url)
    response['Location'] += '#my-anchor'  # добавляем якорь для скроллинга

    return response


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id = basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])