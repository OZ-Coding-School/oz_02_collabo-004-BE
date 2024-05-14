from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields=['user_id','challenge_info_id','amount','merchant_uid','created_at']