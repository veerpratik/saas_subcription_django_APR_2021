from django.db import models

# Create your models here.
from django.db import models


from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

from djstripe.models import Customer, Subscription

from common_account import constants

class UserManager(BaseUserManager):


    def create_manager(self, email, password=None):
        """
                Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.type = constants.MANAGER
        user.set_password(password)
        user.save(using=self._db)  
        return user

    
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,  password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):

    
    USER_TYPE = (
        (constants.ADMIN, 'ADMIN'),
        (constants.MANAGER, 'MANAGER'),
        (constants.EMPLOYEE, 'EMPLOYEE')
        
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    type = models.IntegerField(choices=USER_TYPE, default=constants.MANAGER)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    subscription = models.ForeignKey(Subscription, null=True, blank=True,on_delete=models.SET_NULL)

    objects = UserManager()

    USERNAME_FIELD = 'email'
  

    class Meta:
        db_table = 'user' 
        app_label = 'common_account'

    
    def get_full_name(self):
        # The user is identified by their username 
        return self.email

    def get_short_name(self):
        # The user is identified by their username
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property  #change orignal behaviour of method and call this method just is_staff not required "()" brackets
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_superuser 





