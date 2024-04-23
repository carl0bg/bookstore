from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import View, TemplateView, FormView
from common.utils import TitleMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView

from users.models import User, EmailVerification
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from products.models import Basket

from django.core.mail import send_mail
import string
import secrets
import uuid
from store import settings
from django.core.cache import cache
import gettext

_ = gettext.gettext



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


# def registration(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(data = request.POST)
#         if form.is_valid():
#             form.save() #сохраняем даныне в базе данных
#             messages.success(request, 'Поздравляем! Вы успешно зарегестрировались!')
#             return HttpResponseRedirect(reverse('users:login'))
#     else: 
#         form = UserRegistrationForm()
#     context = {'form': form}
#     return render(request, 'users/registration.html', context)


# class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
#     model = User
#     form_class = UserRegistrationForm
#     template_name = 'users/registration.html'
#     success_url = reverse_lazy('users:login')
#     success_message = 'Вы успешно зарегестрированы!'
#     title = 'Store - Регистрация'


class UserRegistrationView(FormView):
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')


    def form_valid(self, form):
        user, created = User.objects.get_or_create(username = form.cleaned_data['username'])
        new_pass = None

        if created:
            alphabet = string.ascii_letters + string.digits
            new_pass = ''.join(secrets.choice(alphabet) for i in range(8))
            user.set_password(new_pass)
            user.save(update_fields=["password", ])

        if new_pass or user.is_verified_email is False:
            token = uuid.uuid4().hex
            redis_key = settings.C_USER_CONFIRMATION_KEY.format(token=token)
            cache.set(redis_key, {"user_id": user.id}, timeout=settings.C_USER_CONFIRMATION_TIMEOUT)

            confirm_link = self.request.build_absolute_uri(
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
        return super().form_valid(form)




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


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Store - Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user = user, code = code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))

