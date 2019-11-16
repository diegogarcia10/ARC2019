from django.urls import path
from apps.hospital.views import *

urlpatterns = [
	path('',index,name="index4"),
	path('index',index,name="index"),
	path('base2',index2,name="index2"),
	path('base2/<id_tipo>',index3,name="index3"),
]