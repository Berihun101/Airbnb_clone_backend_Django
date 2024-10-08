from django.db import models
import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin, UserManager
# Create your models here.

class CustomUserManager(UserManager):
    def _create_user(self, name, email, password, **extra_fields):
        if not email:
            raise ValueError('you have to specify a valid email')
        email = self.normalize_email(email) 
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user
    def create_user(self,name=None,email=None,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',False)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(name,email,password,**extra_fields)
    
    def create_superuser(self,name,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self._create_user(name,email,password,**extra_fields)
            
class User(AbstractBaseUser,PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="uploads/avaars")

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]

    def __str__(self):
        return self.email
    
    def avatar_url(self):
        if self.avatar:
            return f'{settings.MEDIA_URL}{self.avatar.url}'
        return None