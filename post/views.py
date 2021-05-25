from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import  action
from rest_framework.parsers import ParseError
from .serializers import MaintitleSerializer,SubtitleSerializer, CategorySerializer
from post.models import MainTitle, SubTitle, Category
from user.models import User
from rest_framework import filters
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
import jwt
from rest_framework.permissions import IsAuthenticated,AllowAny

class MaintitleApi(viewsets.ModelViewSet):
    queryset = MainTitle.objects.all()
    serializer_class = MaintitleSerializer
    # permission_classes = (IsAuthenticated,)
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    # def get_permissions(self):
    #     if self.action in ['create','update', 'partial_update', 'destroy']:
    #         self.permission_classes = [IsAuthenticated, ]
    #     elif self.action in ['list']:
    #         self.permission_classes = [AllowAny, ]
    #     return super().get_permissions()

        # def create(self, request, **kwargs):
        #    if self.request.user.is_verified:
        #        serializer = MaintitleSerializer(data=request.data)
        #        if serializer.is_valid():
        #            serializer.save(author=request.user)
        #            return Response(serializer.data, status.HTTP_201_CREATED)

    @action(detail=True, methods=['POST'])
    def upload_image(request):
        try:
            file = request.data['file']
        except KeyError:
            raise ParseError('Request has no resource file attached')
        MainTitle.objects.create(image=file)

    def get(self, **kwargs):
        queryset = MainTitle.objects.all()
        main = MaintitleSerializer(queryset, many=True, context=self.context).data
        return main

class SubtitleApi(viewsets.ModelViewSet):
    queryset = SubTitle.objects.all()
    serializer_class = SubtitleSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    # def get_permissions(self):
    #     if self.action in ['create','update', 'partial_update', 'destroy']:
    #         self.permission_classes = [IsAuthenticated, ]
    #     elif self.action in ['list']:
    #         self.permission_classes = [AllowAny, ]
    #     return super().get_permissions()

    @action(detail=True, methods=['POST'])
    def upload_image(request):
        try:
            file = request.data['file']
        except KeyError:
            raise ParseError('Request has no resource file attached')
        subtitle = SubTitle.objects.create(image=file)

class CategoryApi(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']