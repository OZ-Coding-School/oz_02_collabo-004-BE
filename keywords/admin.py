from django.contrib import admin
from .models import Keyword

@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    pass