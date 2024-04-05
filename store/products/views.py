from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from products.models import Product, ProductCategory, Basket
from users.models import User


def index(request):
    # return HttpResponse('Hello bith')
    context = {
        'title':'Bookstore',
    }
    return render(request, 'products/index2.html', context=context)


def products(request, category_id=None, page_number=1): #может и не быть category id, поэтому None
    # if category_id:
    #     # category = ProductCategory.objects.get(id = category_id)
    #     products = Product.objects.filter(category_id = category_id)
    # else:
    #     products = Product.objects.all()

    products = Product.objects.filter(category_id = category_id) if category_id else Product.objects.all()
   
    per_page = 3 #это сколько товаров продут показано
    paginator = Paginator(products, per_page)
    products_paginator = paginator.page(page_number)
    
    context = {
        'title':'Store - Каталог',
        'products': products_paginator,
        'categories': ProductCategory.objects.all(),
    }    
    return render(request, 'products/products.html', context)


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