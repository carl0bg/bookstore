from django.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail
from django.utils.timezone import now


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null = True, blank = True)
    is_verified_email= models.BooleanField(default=False)


class EmailVerification(models.Model):
    user = models.ForeignKey(to = User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    # code = models.UUIDField(unique=True, default = uuid.uuid4)
    code = models.UUIDField(unique=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'EmailVerification object for {self.user.email}'
    
    def send_verification_email(self):
        link = reverse('users:email_verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        # verification_link = request.META['HTTP_HOST']
        subjects = f'Подтверждение учетной записи для {self.user.username}'
        message = f'Для подтверждения учетной записи для {self.user.email} перейдите по ссылке: {verification_link}'
        
        send_mail(
            subject=subjects,
            message=message,
            from_email=settings.EMAIL_HOST_USER, #default=DEFAULT_FROM_EMAIL
            recipient_list=[self.user.email],
            fail_silently=False, #вызов ошибки
        )

    def is_expired(self): #срок заканчивания 
        return True if now() >= self.expiration else True


