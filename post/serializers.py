from rest_framework import serializers
from .models import MainTitle,SubTitle
from django.template.defaultfilters import slugify

class SubtitleSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(required = False)
    class Meta:
        model = SubTitle
        fields = ['id','title','slug','image','description','created_on','available_on','maintitle']
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class MaintitleSerializer(serializers.ModelSerializer):
    author = serializers.CharField( source="author.username", read_only=True)
    subtitle = SubtitleSerializer(many=True,read_only=True)

    image = serializers.ImageField(required = False)
    class Meta:
        model = MainTitle
        fields=['id','url','author','title','slug','image','description','created_on','subtitle']
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

