from django.urls import path,include
from rest_framework.routers import DefaultRouter
from post import views

router = DefaultRouter()

router.register('maintitle', views.MaintitleApi, basename='maintitle')
router.register('subtitle', views.SubtitleApi, basename='subtitle')
router.register('category', views.CategoryApi, basename='category')


urlpatterns = [
    path('api/',include(router.urls)),
]
