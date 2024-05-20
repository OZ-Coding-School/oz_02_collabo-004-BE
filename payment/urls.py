from django.contrib import admin
from django.urls import path,include
from .views import PaymentView,PaymentListView
urlpatterns = [
   path('payments/<int:user_id>',PaymentListView.as_view(),name='payments'),
   path('payment/<int:pk>',PaymentView.get,name='get'),
   path('payment/create',PaymentView.as_view(),name='post'),
   path('payment/delete',PaymentView.as_view(),name='delete')
]