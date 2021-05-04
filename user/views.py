from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import status,viewsets,generics
from rest_framework.response import Response
from rest_framework.views import APIView
from user.serializers import NewUserSerializer,UserDetailSerializer,MyTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from user.models import User
from user.utils import Util
import jwt
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.

class RegisterAPIView(generics.GenericAPIView):
    serializer_class = NewUserSerializer

    def post(self,request):
        user = request.data
        serializer  = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token
        relativeLink = reverse('email-verify')
        current_site = get_current_site(request).domain
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'hi '+user.first_name+' Use link below\n' +absurl
        data ={
            'email_body': email_body,
            'email_subject':'Verify Your Email',
            'to_email':user.email
        }
        Util.send_email(data)

        return Response(user_data,status=status.HTTP_201_CREATED)

class Verify_Email(generics.GenericAPIView):
    def get(self,request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_active:
                user.is_active = True
                user.save()
                return Response({'email':'Successfully verified email'},status=status.HTTP_201_CREATED)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error':'token expired'},status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error':'Invalid Token'},status=status.HTTP_400_BAD_REQUEST)

class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        NewUser = get_object_or_404(queryset, pk=pk)
        serializer = UserDetailSerializer(NewUser)
        return Response(serializer.data)

class ObtainTokenPairWithUsernameView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
