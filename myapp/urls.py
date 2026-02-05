from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('delete/<CName>',views.delete_city,name='DCity')
]