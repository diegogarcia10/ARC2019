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
    url(r'^sistemaMedicionList/$',login_required(sistemaMedicionList),name="sistemaMedicionList"),
    url(r'^sistemaMedicionCreate/$',login_required(sistemaMedicionCreate), name='sistemaMedicionCreate'),
    path('sistemaMedicionEdit/<str:cod_sistema>/',login_required(sistemaMedicionEdit), name='sistemaMedicionEdit'),
    url(r'^medicoList/$',login_required(medicoList),name="medicoList"),
    url(r'^medicoCreate/$',login_required(medicoCreate), name='medicoCreate'),
    path('medicoEdit/<str:cod_medico>/',login_required(medicoEdit), name='medicoEdit'),

    path('expedienteDetails/<str:cod_paciente>/<str:tipoPersona>',login_required(expedienteDetails), name='expedienteDetails'),
    path('consultaDetails/<str:cod_consulta>/<str:tipoPersona>',login_required(consultaDetails), name='consultaDetails'),

	#FIN URLS MARCO

    #ROSA************
    url(r'^resepcionistaList/$',login_required(resepcionistaList),name="resepcionistaList"),
    url(r'^resepcionistaCreate/$',login_required(resepcionistaCreate), name='resepcionistaCreate'),
    path('resepcionistaEdit/<str:cod_resepcionista>/',login_required(resepcionistaEdit), name='resepcionistaEdit'),
    url(r'^atenderPacientesList/$',login_required(atenderPacientesList),name="atenderPacientesList"),
    path('expedienteDetailsPaciente/<str:cod_paciente>/<str:tipoPersona>',login_required(expedienteDetailsPaciente), name='expedienteDetailsPaciente'),
    path('consultaDetailsPaciente/<str:cod_consulta>',login_required(consultaDetailsPaciente), name='consultaDetailsPaciente'),
    path('consultaCreate/<str:cod_paciente>',login_required(consultaCreate), name='consultaCreate'),
    path('recetaCreate/<str:cod_consulta>',login_required(recetaCreate), name='recetaCreate'),
    #****************
    #Parte Diego
    path('registrarEntrada',registrar_entrada,name="registrar_entrada"),
    path('captura',captura,name="captura"),
    path('registrar-paciente/<str:id_tarjeta>',crear_paciente,name="registrar_paciente"),
    path('list-paciente',list_paciente,name="list_paciente"),
    path('cambiar-codigo/<str:cod_antiguo>',cambiar_codigo,name="cambiar_codigo"),
    path('capturaCambio',captura_changue,name="captura_changue"),
    path('list-citas',list_citas,name="list_citas"),
    path('nueva-cita',nueva_cita,name="nueva_cita"),
    path('capturaCita',captura_cita,name="captura_cita"),
    path('registrar-cita/<str:id_paciente>',registar_cita,name="registar_cita"),

    #url para las peticiones ajax
    path('busqueda_medicos',busqueda_medico,name="busqueda_medico"),
    path('select_medico',select_medico,name="seleccion_medico"),
    path('alg_hora',alg_hora,name="alg_hora"),
    path('confirmar_cita',confirmar_cita,name="confirmarcita")
    #Fin parte Diego
    
]