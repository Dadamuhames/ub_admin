from django.contrib import admin
from .models import Messages, SearchQuoteGroup, SearchQuotes
from django.contrib.auth.models import Permission
# Register your models here.



admin.site.register(Messages)
admin.site.register(SearchQuoteGroup)
admin.site.register(SearchQuotes)