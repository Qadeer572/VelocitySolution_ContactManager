from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Catagory(models.Model):
    id = models.AutoField(primary_key=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories', null=True, blank=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

     

class Contact(models.Model):
    id= models.AutoField(primary_key=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts', null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    Catagory = models.ForeignKey(Catagory, on_delete=models.CASCADE, related_name='contacts')
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name



class Activity(models.Model):
    id= models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', null=True, blank=True)
    activity_type = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    activity_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.activity_type} - {self.user.username} on {self.activity_date.strftime('%Y-%m-%d %H:%M:%S')}"