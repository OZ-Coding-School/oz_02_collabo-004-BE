from django.contrib import admin
from django.urls import path,include
from .views import PaymentView
urlpatterns = [
   path('payments/<int:user_id>',PaymentView.as_view())
]
