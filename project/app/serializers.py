from rest_framework import serializers
from django.conf import settings
from app.models import Profile,CustomUser,InvitationStatus,Guest
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from PIL import Image
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

class GuestSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='invitation_status.status')
    class Meta:
        model = Guest
        fields = ['name','email','status']

    def create(self,validated_data):
        invitation,c = InvitationStatus.objects.get_or_create(status = validated_data.pop('invitation_status')['status'])
        guest = Guest.objects.create(name = validated_data['name'],email = validated_data['email'],invitation_status = invitation)
        return guest

class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvitationStatus
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['user','created_at','guests']

    def update(self, instance, validated_data):
        # MANIPULATE DATA HERE BEFORE INSERTION

        instance = super(ProfileSerializer, self).update(instance, validated_data)
        if instance.profile_pic:
            image = Image.open(instance.profile_pic)
            height, width = image.size
            aspect_ratio = width/height
            print("image size")
            print(image.size)
            if width <= 300:
                image.close()
                return instance
            new_width = 300
            new_height = new_width/aspect_ratio
            image = image.resize((new_width,int(new_height)), Image.NEAREST)
            print("image size")
            print(image.size)
            image.save(instance.profile_pic.path)
            image.close()
        return instance


