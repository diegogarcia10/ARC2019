from django.urls import path
from apps.hospital.views import *
urlpatterns = [
	path('index',index,name="index"),
]