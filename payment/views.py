from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from .serializers import PaymentSerializer
import datetime
#올릴떈 민감정보 숨기기

class PaymentView(APIView):
    

    def create_payment(self,request):

        payment = Payment.objects.create(
            user=request.user,
            challengeInfo=request.name,
            price=request.amount,
            timestamp=datetime.now(),
            imp_uid='imp40371015'
        )
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

