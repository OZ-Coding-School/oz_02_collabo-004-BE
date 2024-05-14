
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Payment
from payment.serializers import PaymentSerializer
import datetime
from django.views.decorators.csrf import csrf_exempt
from iamport import Iamport
#올릴떈 민감정보 숨기기

class PaymentView(APIView):

    def post(self,request):
        iamport= Iamport(imp_key="1114627331688245",imp_secret='BjPMCjOUDprlS0nhO37wFZqfFmFMda5CkSuubC4PgADWrUXpnZ4741NaVDt2ziXu7IAi3MpkjTyMRoaB')
        payment_data=request.data
        serializer = PaymentSerializer(data=payment_data)
        if serializer.is_valid():
            serializer.save(user_id=payment_data.get('user'),challenge_info_id=payment_data.get('challenge_info'))
            response = iamport.payment(payment_data)
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    def delete(self,request):
        iamport=Iamport()
        data=request.data
        imp_uid= data.get('imp_uid')

        iamport.cancel(imp_uid=imp_uid)
        serializer = PaymentSerializer(data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    @api_view(['GET',])
    def get(self,pk):
        payment_data= Payment.objects.filter(pk=pk).first()
        serializer = PaymentSerializer(payment_data)
    
        return Response(data=serializer.data)

class PaymentListView(APIView):
    @api_view(['GET',])
    def get(self):
        pay= Payment.objects.all()
        serializers = PaymentSerializer(pay,many=True)
        return Response(data=serializers.data)