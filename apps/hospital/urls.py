from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.conf.urls import url, include
from apps.hospital.views import *
from django.contrib.auth.views import login

app_name="hospital"
urlpatterns = [
	path('',index,name="index4"),
	path('index',index,name="index"),
	path('base2',index2,name="index2"),
	path('base2/<id_tipo>',index3,name="index3"),

	#INICIO URLS MARCO
	url(r'^especialidadList/$',login_required(especialidadList),name="especialidadList"),
	url(r'^especialidadCreate/$',login_required(especialidadCreate), name='especialidadCreate'),
    path('especialidadEdit/<str:cod_especialidad>/',login_required(especialidadEdit), name='especialidadEdit'),
    url(r'^medicamentoList/$',login_required(medicamentoList),name="medicamentoList"),
    url(r'^medicamentoCreate/$',login_required(medicamentoCreate), name='medicamentoCreate'),
    path('medicamentoEdit/<str:cod_medicamento>/',login_required(medicamentoEdit), name='medicamentoEdit'),
	#FIN URLS MARCO
]