from common_account import constants
from django.db import models

class Manager(models.Model):
    
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120,null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    company = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length = 200,null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

  
    def __str__(self):
        return self.first_name

    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name
