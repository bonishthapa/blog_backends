from rest_framework import serializers
from user.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class NewUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, style = {'input_type': 'password'})

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ['email','first_name','last_name','password']
        read_only_fields = ('is_active','is_verified')


        # def create(self, validated_data):
        #     user = User(
        #         email=validated_data['email'],
        #         username=validated_data['username']
        #     )
        #     user.set_password(validated_data['password'])
        #     user.save()
        #     return user

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields=['email','first_name','password','is_active','is_staff']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        return token
