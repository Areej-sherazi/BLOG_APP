from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from rest_framework.authtoken.models import Token

import random

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=6, blank=True, null=True)
    code_expiry = models.DateTimeField(null=True, blank=True)
    code_attempts = models.PositiveIntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] 

    MAX_CODE_ATTEMPTS = 2
    CODE_EXPIRY_MINUTES = 36000

    def is_code_expired(self):
        return self.code_expiry is None or self.code_expiry < timezone.now()

    def can_resend_code(self):
        return self.code_attempts < self.MAX_CODE_ATTEMPTS

    def generate_new_code(self):
        self.code = self.generate_new_6_digit_code()
        self.code_expiry = timezone.now() + timezone.timedelta(minutes=self.CODE_EXPIRY_MINUTES)
        self.code_attempts += 1

    def generate_new_6_digit_code(self):
        return str(random.randint(100000, 999999))


    def reset_code_attempts(self):
        self.code_attempts = 0

    # Specify unique related names for groups and user_permissions
    groups = models.ManyToManyField('auth.Group', related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='customuser_set', blank=True)

# @receiver(post_save, sender=User)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)

# post_save.connect(create_auth_token, sender=User)
