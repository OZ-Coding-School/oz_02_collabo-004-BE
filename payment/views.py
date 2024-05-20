
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Payment
import requests
from payment.serializers import PaymentSerializer
import datetime
from django.views.decorators.csrf import csrf_exempt
from iamport import Iamport
#올릴떈 민감정보 숨기기
IAMPORT_REST_API_KEY="1114627331688245"
IAMPORT_REST_API_SECRET='BjPMCjOUDprlS0nhO37wFZqfFmFMda5CkSuubC4PgADWrUXpnZ4741NaVDt2ziXu7IAi3MpkjTyMRoaB'
class PaymentView(APIView):

    def post(self,request):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'imp_apikey {IAMPORT_REST_API_KEY}:{IAMPORT_REST_API_SECRET}'
        }
        payment_data=request.data
        serializer = PaymentSerializer(data=payment_data)
        if serializer.is_valid():
            serializer.save(user_id=payment_data.get('user'),challenge_info_id=payment_data.get('challenge_info'))
            response = requests.post('https://api.iamport.kr/payments/prepare', json=payment_data, headers=headers)
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
    
    def get(self,request,user_id):
        pay= Payment.objects.filter(user_id=user_id)
        serializers = PaymentSerializer(pay,many=True)
        return Response(data=serializers.data)