from django.db import models

# Create your models here.
class Customer(models.Model):
    first_name=models.CharField(max_length=16,null=True)
    last_name=models.CharField(max_length=16, null=True)
    email = models.EmailField(unique= True,null = True)
    password=models.CharField(max_length = 15,null=True)
    confirm_password=models.CharField(max_length = 15,null=True)
    
    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)