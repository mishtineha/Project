from django.shortcuts import render
from rest_framework.views import APIView
from app.serializers import UserSerializer,LoginSerializer,GuestSerializer,StatusSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from app.models import InvitationStatus

User = get_user_model()

class RegisterView(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'successs','message':'user created successfully'})
        return Response({'status':'errors','message':serializer.errors})

class LoginView(APIView):
    def post(self,request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(**serializer.validated_data)
            except:
                return Response({'status':'error','message':'unable to login with provided credential'})
            token,c = Token.objects.get_or_create(user = user)
            return Response({'status':'success','message':'successfully loggedin','token':token.key})
        return Response({'status':'errors','message':serializer.errors})

class GuestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        serializer = GuestSerializer(instance = request.user.profile.guests,many = True)
        return Response({'status':'success','data':serializer.data,'message':'list of all guest'})
    def post(self,request):
        serializer = GuestSerializer(data = request.data)
        if serializer.is_valid():
            guest = serializer.save()
            request.user.profile.guests.add(guest)
            return Response({'status':'success','message':'guest created successfully'})
        return Response({'status':'errors','message':serializer.errors})

class StatusView(APIView):
    def get(self,request):
        serializer = StatusSerializer(instance = InvitationStatus.objects.all(),many=True)
        return Response({'status': 'success', 'data': serializer.data, 'message': 'all status'})





# Create your views here.
