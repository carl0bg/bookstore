from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import View

from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from products.models import Basket

# Create your views here.


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data = request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username = username, password = password) #сравним есть ли такой пользователь
            if user:
                auth.login(request, user) #если пользователь есть, мы его авторизовали
                return HttpResponseRedirect(reverse('index')) #перенаправляем на главную страницу
    else:
        form = UserLoginForm()  
    context = {'form': form}
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data = request.POST)
        if form.is_valid():
            form.save() #сохраняем даныне в базе данных
            messages.success(request, 'Поздравляем! Вы успешно зарегестрировались!')
            return HttpResponseRedirect(reverse('users:login'))
    else: 
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/registration.html', context)


'''
@login_required
def profile(request):
   if request.method == 'POST': #меняем имя, если захотим редактировать
      form = UserProfileForm(instance = request.user, data = request.POST, files = request.FILES) #если заполним новые данные
      if form.is_valid():                                                  #это чтобы прикрепить фотографию
         form.save()
         return HttpResponseRedirect(reverse('users:profile'))
      else:
         print(form.errors) #выводим в консоль ошибки
   else:
      form = UserProfileForm(instance = request.user) #сделано чтобы отображать данные в полях 

   context = { 'title': 'Store-Профиль',
               'form': form, 
               'baskets': Basket.objects.filter(user = request.user),
               # 'total_sum': total_sum, 
               # 'total_quantity': total_quantity
   } #нужно делать с фильтром, потому что будут видны все товары, добавленные даже другими пользоватлеями
   #print(Product.objects.all().order_by('name'))
   return render(request, 'users/profile.html', context)
'''

class profile(View):
    template_name = 'users/profile.html'
    context = {'title': 'Store-Профиль'}

    def get(self, request, *args, **kwargs):
        form = UserProfileForm(instance = request.user)
        self.context.update(form=form, baskets = Basket.objects.filter(user = request.user))
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = UserProfileForm(instance = request.user, data = request.POST, files = request.FILES)
        if form.is_valid():                                                
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            print(form.errors) #выводим в консоль ошибку
            # self.context.update(form=form, baskets=Basket.objects.filter(user=request.user))
            return render(request, self.template_name, self.context)
            

def logout(request):
    auth.logout(request) #пользователь выйдет из системы
    return HttpResponseRedirect(reverse('index'))

