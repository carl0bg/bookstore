from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import View, TemplateView, FormView
from common.utils import TitleMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView

from users.models import User #, EmailVerification
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from products.models import Basket

#for email
from django.core.mail import send_mail
import string
import secrets
import uuid
from store import settings
from django.core.cache import cache
import gettext
_ = gettext.gettext


from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.forms import model_to_dict
from .serializers import UserSerializer


class APIView(APIView):
    def get(self, request):
        # lst = User.objects.all().values()
        # return Response({'stat': list(lst)})
        u = User.objects.all() #формируется список обьектов
        return Response({'posts': UserSerializer(u, many= True).data}) #many-список записей обрабатывать #по факту как наш encode

    
    def post(self, request):
        serializer = UserSerializer(data= request.data)
        serializer.is_valid(raise_exception=True) #проверяем по UserSerial валидатность

        serializer.save() #автоматически вызовет UserSerializer.create

        return Response({'post': serializer.data}) #model_to_dict - преобразует в словарь
    
    def put(self, request, *args, **kwargs):
        print(f'kwargs {kwargs}')
        pk = kwargs.get("pk", None)
        print(f'pk {pk}')
        if not pk:
            return Response({"error": "Method PUT not allowed"})
        
        try:
            instance = User.objects.get(pk = pk)
            print(f'inst {instance}')
        except:
            return Response({"error": "Method PUT not exists"})
        
        serializer = UserSerializer(data = request.data, instance= instance)
        print(f'serial {serializer}')
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"post": serializer.data})




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


def form_email(request, form):
        user, created = User.objects.get_or_create(username = form.cleaned_data['username'])
        print(user.email, user.username)
        new_pass = None


        if user.is_verified_email is False:
            alphabet = string.ascii_letters + string.digits
            new_pass = ''.join(secrets.choice(alphabet) for i in range(8))
            print(f'new_pass {new_pass}')
            user.set_password(new_pass)
            user.save(update_fields=["password", ])



            token = uuid.uuid4().hex
            print(f'token = {token}')
            redis_key = settings.C_USER_CONFIRMATION_KEY.format(token=token)
            print(f'redis = {redis_key}')
            cache.set(redis_key, {"user_id": user.id}, timeout=settings.C_USER_CONFIRMATION_TIMEOUT)

            confirm_link = request.build_absolute_uri(
                reverse_lazy(
                    "users:register_confirm", kwargs={"token": token}
                )
            )
            message = _(f"follow this link %s \n"
                        f"to confirm! \n" % confirm_link)
            if new_pass:
                message += f"Your new password {new_pass} \n "

            send_mail(
                subject= "Please confirm your registration!",
                message=message,
                from_email="carlbg000@yandex.ru",
                recipient_list=[user.email, ]
            )


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data = request.POST)
        if form.is_valid():
            # form_email(request= request, form = form)
            form.save() #сохраняем даныне в базе данных
            form_email(request=request, form = form)
            messages.success(request, 'Поздравляем! Вы успешно зарегестрировались!')
            return HttpResponseRedirect(reverse('users:login'))
    else: 
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/registration.html', context)




def register_confirm(request, token):
    redis_key = settings.C_USER_CONFIRMATION_KEY.format(token=token)
    user_info = cache.get(redis_key) or {}

    if user_id := user_info.get("user_id"):
        user = get_object_or_404(User, id=user_id)
        user.is_verified_email = True
        user.save(update_fields=["is_verified_email"])
        return redirect(to=reverse_lazy("users:profile"))
    else:
        return redirect(to=reverse_lazy("users:registration"))




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



