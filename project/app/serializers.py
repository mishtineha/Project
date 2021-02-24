from rest_framework import serializers
from django.conf import settings
from app.models import Profile,CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
# User = settings.AUTH_USER_MODEL
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required = True)
    phone = serializers.IntegerField(required = True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['name','email','password','password2','phone']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self,validated_data):
        name = validated_data.pop('name')
        phone = validated_data.pop('phone')
        validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        Profile.objects.create(user = user,name=name,contact_number = phone)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)
    password = serializers.CharField(required=True)


