from django.db import models
import re


class Usermanager(models.Manager):
    def validate(self,data):
        errors ={}
        if len(data['name']) < 5 or not data['name'].isalpha():
            errors['name'] ='The first name must be more than five characters , and must contian only characters!'
        if len(data['company']) < 3 :
            errors['company'] = 'You should inter a valid company name !'
        if data['password'] != data['conf_password']:
            errors['password'] = 'The Password didnt match !'
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(data['email']):
            errors['email'] = 'Inavalid Email !'
        user = Users.objects.filter(email = data['email'])
        if user:
            errors['exist_email'] = 'The email entred is alredy exist !'
        company = Users.objects.filter(company = data['company'])
        if company :
            errors['exist_company'] = 'The name of the company is alredy exist !'
        return errors

class Users(models.Model):
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=512)
    phone = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Usermanager()
# Create your models here.

class Images(models.Model):
    url = models.TextField()
    user = models.ForeignKey(Users,related_name='image',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Videos(models.Model):
    url = models.TextField()
    user = models.ForeignKey(Users,related_name='video',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MessagesFromUser(models.Model):
    message = models.TextField()
    user = models.ForeignKey(Users,related_name='message',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
