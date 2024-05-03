from .models import Basket

def baskets(request):
    user = request.user
    print('тут бывал...................')
    return {'baskets': Basket.objects.filter(user = user) if user.is_authenticated else []}