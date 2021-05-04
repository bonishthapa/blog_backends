from django.urls import path,include
from user import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('api/register/', views.RegisterAPIView.as_view()),
    path('email-verify',views.Verify_Email.as_view(),name='email-verify'),

    path('api/user/list/',views.UserViewSet.as_view({'get': 'list'})),
    path('api/user/detail/<int:pk>',views.UserViewSet.as_view(({'get': 'retrieve'}))),


    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('logout/blacklist/', views.BlacklistTokenUpdateView.as_view(),name='blacklist'),

    path('token', views.ObtainTokenPairWithUsernameView.as_view()),
]
