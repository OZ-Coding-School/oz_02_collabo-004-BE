from django.contrib import admin
from .models import ChallengeSpoiler

@admin.register(ChallengeSpoiler)
class ChallengeSpoilerAdmin(admin.ModelAdmin):
    pass