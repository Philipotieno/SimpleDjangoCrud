from django.urls import path

from .views import (ListCreateInstitutions, ListCreateHead, ListCreateReport)

urlpatterns = [
    path('add-institution/', ListCreateInstitutions.as_view(), name='add-institutions'),
    path('list-institutions/', ListCreateInstitutions.as_view(), name='list-institutions'),
    # path('<int:id>/', RetreiveCamp.as_view(), name='get-one-camp'),
    path('update-institutions/<int:id>/', ListCreateInstitutions.as_view(), name='update-institution'),
    path('delete-camp/<int:id>/', ListCreateInstitutions.as_view(), name='delete-camp'),
    path('<int:id>/add-head/',
         ListCreateHead.as_view(), name='add-commnder'),
    path('list-heads/', ListCreateHead.as_view(), name='list-commnders'),
    # path('head/<int:id>/', RetreiveHead.as_view(),
        #  name='get-one-head'),
    path('update-head/<int:id>/',
         ListCreateHead.as_view(), name='update-commnders'),
    path('delete-head/<int:id>/',
         ListCreateHead.as_view(), name='delete-commnders'),

]