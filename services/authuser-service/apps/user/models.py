from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin 


class UserManager(BaseUserManager):
    
    def create_user(self, email, password = None, **extra_fields):
        if not email:
            raise ValueError('Введите mail !')
        
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='users/avatars/', null=True, blank=True)
    date_joined = models.DateTimeField( auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):

        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):

        return self.first_name
