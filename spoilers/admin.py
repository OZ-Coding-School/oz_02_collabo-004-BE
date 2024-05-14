from django.contrib import admin
from .models import Spoiler

@admin.register(Spoiler)
class SpoilerAdmin(admin.ModelAdmin):
    pass