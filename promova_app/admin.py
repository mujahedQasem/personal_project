from django.contrib import admin

from promova_app.models import *

class UserAdmin(admin.ModelAdmin):
    list_filter = ['created_at']
    

class MessageAdmin(admin.ModelAdmin):
    list_filter = ['user']

admin.site.register(Users,UserAdmin)

admin.site.register(MessagesFromUser,MessageAdmin)

# Register your models here.
