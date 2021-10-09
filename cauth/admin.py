from django.contrib import admin

from .models import Account, Session
admin.site.register(Account)
admin.site.register(Session)