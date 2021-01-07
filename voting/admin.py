from django.contrib import admin
from django.contrib.admin import AdminSite

# Register your models here.
class MyAdminSite(AdminSite):
    login_template = 'voting/login.html'

site = MyAdminSite()