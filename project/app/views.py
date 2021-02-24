from django.shortcuts import render
from rest_framework.views import APIView
from app.serializers import UserSerializer,LoginSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

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




# Create your views here.
