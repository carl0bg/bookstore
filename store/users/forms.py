from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from users.models import User
from django import forms

# from users.tasks import send_email_verification


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
      'class':"form-control py-4",
      'placeholder': "Введите имя пользователя",
   }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
      'class':"form-control py-4",
      'placeholder':"Введите пароль",
   }))
    class Meta:
        model = User
        fields = ('username', 'password')
        

# class UserRegistrationForm(UserCreationForm):
#     first_name = forms.CharField(widget=forms.TextInput(attrs={
#          'class':"form-control py-4",
#          'placeholder': "Введите имя"}))
#     last_name = forms.CharField(widget=forms.TextInput(attrs={
#          'class':"form-control py-4",
#          'placeholder': "Введите фамилию"}))
#     username = forms.CharField(widget=forms.TextInput(attrs={
#          'class':"form-control py-4",
#          'placeholder': "Введите имя пользователя"}))
#     email = forms.CharField(widget=forms.EmailInput(attrs={
#          'class':"form-control py-4",
#          'placeholder': "Введите почту"}))      
#     password1 = forms.CharField(widget=forms.PasswordInput(attrs={
#          'class':"form-control py-4",
#          'placeholder': "Введите пароль"}))     
#     password2 = forms.CharField(widget=forms.PasswordInput(attrs={
#          'class':"form-control py-4",
#          'placeholder': "Подтвердите пароль"}))               

#     class Meta:
#          model = User
#          fields = ('first_name', 'last_name', 'username','email', 'password1', 'password2')

#     def save(self, commit = True):
#         user = super(UserRegistrationForm, self).save(commit=True)
#         send_email_verification(user.id)
#         return user
    
class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
         'class':"form-control py-4",
         'placeholder': "Введите имя"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
         'class':"form-control py-4",
         'placeholder': "Введите фамилию"}))
    username = forms.CharField(widget=forms.TextInput(attrs={
         'class':"form-control py-4",
         'placeholder': "Введите имя пользователя"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
         'class':"form-control py-4",
         'placeholder': "Введите почту"}))      
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
         'class':"form-control py-4",
         'placeholder': "Введите пароль"}))     
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
         'class':"form-control py-4",
         'placeholder': "Подтвердите пароль"}))  
    
     
    class Meta:
         model = User
         fields = ('first_name', 'last_name', 'username','email', 'password1', 'password2')


#     def save(self, commit = True):
#         user = super(UserRegistrationForm, self).save(commit=True)
#         return user
    

#     def clean_confirmation(self):
#           if self.cleaned_data['confirmation'] is not True:
#                raise ValidationError('You must confirm!')





class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
         'class':"form-control py-4"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
         'class':"form-control py-4"}))
    image = forms.ImageField(widget=forms.FileInput(attrs={
     'class':"custom-file-input"}), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={
         'class':"form-control py-4", 'readonly':True })) #ставив 'readonly' True - чтобы можно было только посмотреть профиль а не редактировать
    email = forms.CharField(widget=forms.TextInput(attrs={
         'class':"form-control py-4", 'readonly':False }))
    
    
    class Meta:
        model = User
        fields = {'first_name', 'last_name', 'image', 'username', 'email'}