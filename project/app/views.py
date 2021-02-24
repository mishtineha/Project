from django.shortcuts import render
from rest_framework.views import APIView
from app.serializers import UserSerializer
from rest_framework.response import Response

class RegisterView(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'successs','message':'user created successfully'})
        return Response({'status':'errors','errors':serializer.errors})


# Create your views here.
