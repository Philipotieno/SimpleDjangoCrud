from django.urls import path
from .views import (RegistrationAPIView, LoginAPIView, UserRetrieveUpdateAPIView, RetrieveUserProfile)

urlpatterns = [
    path('', RegistrationAPIView.as_view(), name='add-list-user'),
    path('<int:id>/', RegistrationAPIView.as_view(), name='delete-users'),
    path('login/', LoginAPIView.as_view(), name='user-login'),
    path('profile/', UserRetrieveUpdateAPIView.as_view(), name='get-user-profile'),
     path('my-profile/', RetrieveUserProfile.as_view(), name='get-user-profile'),
    path('profile/<int:id>/', UserRetrieveUpdateAPIView.as_view(), name='user-profile'),
]
