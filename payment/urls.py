from django.contrib import admin
from django.urls import path,include

urlpatterns = [
   path('/payments/<int:user_id>')
]
