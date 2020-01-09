from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from apps.hospital.models import *
from apps.hospital.forms import *
#Librerias para calcular edad
from datetime import date
from dateutil.relativedelta import relativedelta

#Librerias Necesarias para la comunicacion con el arduino
import time
import serial
import serial.tools.list_ports
import random

#--------PARTE DE DIEGO--------------#
#Metodo que verifica cual es el puerto en el que esta conectado el arduino
def puerto():
	ports = list(serial.tools.list_ports.comports())
	puerto = ''
	for p in ports:
		puerto = p
	puerto = puerto[0]
	return puerto

#Metodo que retorna el codigo leido por el RFID--> Arduino --> Sistema WEB
def lectura():	
	puerto_asignado = puerto()
	arduino = serial.Serial(puerto_asignado, 9600)
	time.sleep(2)
	codigo=''
	while codigo == '':
		codigo = arduino.readline()
	arduino.close()	
	return codigo

#Metodo que convierte el codigo de la targeta sin espacios por inconvenientes en la base de datos

def sinEspacio(param):
	codigo=str(param)
	nuevo=codigo.replace(' ', '')
	return nuevo 

# Create your views here.
def index(request):
	persona_actual2=""
	if request.user.is_authenticated:		
		return redirect("hospital:index2")
	else:
		return render(request,'base/index.html',{'tipoPersona':persona_actual2})

	

def index2(request):
	tipoPersona=""
	persona_actual2=""
	persona=""
	resepcionista=""
	paciente=""
	medico=""
	if not persona_actual2:
		print("no ha seleccionado que es")
	else:
		print("ya selecciono xD")
	usuario_log=User.objects.get(username=request.user)
	print(usuario_log)
	
	if Persona.objects.filter(usuario=usuario_log).exists():
		#Filtrando los roles de la personas
		persona=Persona.objects.get(usuario=usuario_log)
		print("Existe persona")
		if Resepcionista.objects.filter(cod_persona=persona).exists():
			resepcionista=Resepcionista.objects.get(cod_persona=persona)
			print("Tiene Rol Resepcionista")
		else:
			print("no es Resepcionista")
		if Paciente.objects.filter(cod_persona=persona).exists():
			paciente=Paciente.objects.get(cod_persona=persona)
			print("Tiene rol de Paciente")
		else:
			print("No es Paciente")
		if Medico.objects.filter(cod_persona=persona).exists():
			medico=Medico.objects.get(cod_persona=persona)
			print("Es un Medico")
		else:
			print("No tiene rol de medico") 		
	else:
		print("Nel no existe")

	if 'btnMedico' in request.POST:
			
		print("Esta Precionando el boton de medico")
		return redirect('hospital:index3',1)
	if 'btnPaciente' in request.POST:
		
		print("Esta Precionando el boton de paciente")
		return redirect('hospital:index3',2)
	if 'btnResepcionista' in request.POST:
		
		print("Esta Precionando el boton de Resepcionista")
		return redirect('hospital:index3',3)
	contexto={'paciente':paciente,'medico':medico,'resepcionista':resepcionista,'tipoPersona':tipoPersona}
	return render(request,'base/base2.html',contexto)

def index3(request,id_tipo):
	
	tipoPersona=""
	if id_tipo=="1":
		tipoPersona="1"
		print("Elijio 1")
		print(str(request.user))		
		return render(request,'base/index.html',{'tipoPersona':tipoPersona})
	if id_tipo=="2":
		tipoPersona="2"
		print("Elijio 2")
		print(str(request.user))
		usuario=User.objects.get(username=str(request.user))
		persona=Persona.objects.get(usuario=usuario)
		paciente=Paciente.objects.get(cod_persona=persona)
		contexto={'tipoPersona':tipoPersona,'paciente':paciente}		
		return render(request,'base/index.html',contexto)
	if id_tipo=="3":
		tipoPersona="3"
		print("Elijio 3")
		print(str(request.user))
		return render(request,'base/index.html',{'tipoPersona':tipoPersona})


def registrar_entrada(request):
	tipoPersona="3"
	contexto={'tipoPersona':tipoPersona}
	return render(request,'resepcionista/registrar_entrada.html',contexto)

def captura(request):
	codigo=lectura()
	mensaje=''

	codigo=codigo.decode('utf-8')
	codigo=codigo[1:12]
	codigo=sinEspacio(codigo)
	existencia = Paciente.objects.filter(cod_paciente=codigo).exists()
	if existencia:
		mensaje = 'Paciente encontrado de clic en el boton para ver su expediente, codigo: '+codigo
	else:
		mensaje = 'No hay ningun Paciente asociado a esta tarjeta, intente nuevamente dando clic al boton, codigo: '+codigo 
	print(codigo)
	context={
		'mensaje': mensaje,
		'existencia': existencia,
		'codigo': codigo,
	}
	return render(request, 'resepcionista/pre_crear.html', context)

def crear_paciente(request,id_tarjeta):
	codigo=str(id_tarjeta)
	tipoPersona="3"
	contexto={'tipoPersona':tipoPersona,'codigo':id_tarjeta}

	if request.method=='POST':
		usuario=User()
		persona=Persona()
		paciente=Paciente()
		expediente=Expediente()
		usuario.is_staff=True
		usuario.first_name=request.POST['nombres']
		usuario.last_name=request.POST['apellidos']
		#Creando username DO000		
		concac1=str(usuario.first_name).upper()
		concac1=concac1[0]
		concac2=str(usuario.last_name).upper()
		concac2=concac2[0]
		concac3=codigo[5:8]
		usuario.username=concac1+concac2+concac3
		clave=concac1+concac2+codigo[0:3]
		usuario.set_password(concac1+concac2+concac3)
		usuario.save()
		persona.usuario=usuario
		persona.sexo=Sexo.objects.get(cod_sexo=str(request.POST['sexo']))
		persona.fecha_nacimiento=request.POST['fecha_nacimiento']
		persona.save()
		paciente.cod_paciente=codigo
		paciente.cod_persona=persona
		paciente.save()
		expediente.cod_paciente=paciente
		expediente.save()
		return redirect('hospital:index3',3)		
	return render(request,'paciente/registrar_paciente.html',contexto)


def list_paciente(request):
	pacientes=Paciente.objects.all().order_by('cod_paciente')
	contexto={'tipoPersona':str(3),'pacientes':pacientes}
	return render(request,'paciente/list_paciente.html',contexto)

def cambiar_codigo(request,cod_antiguo):
	tipoPersona="3"
	if request.method=='POST':
		codigo_nuevo=request.POST['codigo']
		paciente=Paciente.objects.get(cod_paciente=str(cod_antiguo))
		paciente.cod_paciente=codigo_nuevo
		paciente.save()
		return redirect('hospital:list_paciente')
	contexto={'tipoPersona':tipoPersona}
	return render(request,'resepcionista/cambiar_codigo.html',contexto)

def captura_changue(request):
	codigo=lectura()
	mensaje=''

	codigo=codigo.decode('utf-8')
	codigo=codigo[1:12]
	codigo=sinEspacio(codigo)
	existencia = Paciente.objects.filter(cod_paciente=codigo).exists()
	if existencia:
		mensaje = 'Lo Sentimos la tarjeta ya esta registrada con otro paciente intente con otra , codigo: '+codigo
	else:
		mensaje = 'Tarjeta Libre de clic en el boton para realizar el cambio, codigo: '+codigo 
	print(codigo)
	context={
		'mensaje': mensaje,
		'existencia': existencia,
		'codigo': codigo,
	}
	return render(request, 'resepcionista/pre_cambiar.html', context)

def captura_cita(request):
	codigo=lectura()
	mensaje=''

	codigo=codigo.decode('utf-8')
	codigo=codigo[1:12]
	codigo=sinEspacio(codigo)
	existencia = Paciente.objects.filter(cod_paciente=codigo).exists()
	if existencia:
		mensaje = 'Paciente encontrado, con el codigo: '+codigo
	else:
		mensaje = 'Paciente no encontrado, de clic en el boton, codigo: '+codigo 
	print(codigo)
	context={
		'mensaje': mensaje,
		'existencia': existencia,
		'codigo': codigo,
	}
	return render(request, 'cita/pre_cita.html', context)

def nueva_cita(request):
	tipoPersona="3"
	contexto={'tipoPersona':tipoPersona}
	return render(request,'cita/nueva_cita.html',contexto)

def list_citas(request):
	citas=Cita.objects.all()
	contexto={'citas':citas,'tipoPersona':str(3)}
	return render(request,'resepcionista/list_citas.html',contexto)


#--------FIN PARTE DE DIEGO--------------#
#view Marco
def especialidadList(request):
	if 'accion' in request.POST:
		accion = request.POST['accion']
		codigo_especialidad = request.POST['especialidad']
		especialidad = Especialidad.objects.get(cod_especialidad = codigo_especialidad)
		if accion == 'Eliminar':	
			especialidad.delete()
			pass
		pass

	especialidad = Especialidad.objects.all().order_by('cod_especialidad')
	contexto = {'especialidades':especialidad}
	return render(request, 'especialidad/especialidadList.html', contexto)	

def especialidadCreate(request):
	if request.method == 'POST':
		especialidad=Especialidad()
		especialidad.cod_especialidad=request.POST['codigo']
		especialidad.nombre_especialidad=request.POST['nombre']
		especialidad.save()
		pass
		return redirect('hospital:especialidadList')
	else:
		return render(request, 'especialidad/especialidadCreate.html')

def especialidadEdit(request, cod_especialidad):
	especialidad = Especialidad.objects.get(pk=cod_especialidad)
	if request.method == 'GET':
		contexto={'especialidad':especialidad}
	else:
		especialidad.nombre_especialidad=request.POST['nombre']
		especialidad.save()
		return redirect('hospital:especialidadList')
	return render(request, 'especialidad/especialidadCreate.html', contexto)

def medicamentoList(request):
	if 'accion' in request.POST:
		accion = request.POST['accion']
		codigo_medicamento = request.POST['medicamento']
		medicamento = Medicamento.objects.get(cod_medicamento = codigo_medicamento)
		if accion == 'Eliminar':	
			medicamento.delete()
			pass
		pass

	medicamento = Medicamento.objects.all().order_by('cod_medicamento')
	contexto = {'medicamentos':medicamento}
	return render(request, 'medicamento/medicamentoList.html', contexto)

def medicamentoCreate(request):
	sistemas = SistemaMedicion.objects.all().order_by('nombre_sistema')
	if request.method == 'POST':
		medicamento = Medicamento()
		medicamento.cod_medicamento=request.POST['codigo']
		medicamento.nombre_medicamento=request.POST['nombre']
		medicamento.farmacia=request.POST['farmacia']
		medicamento.descripcion=request.POST['descripcion']
		medicamento.save()

		for sis in sistemas:
			if 'sis_'+str(sis.cod_sistema) in request.POST:
				medicamento.sistema_medicion.add(sis)
				pass
			pass
		pass
		return redirect('hospital:medicamentoList')
	else:
		contexto={'sistemas':sistemas}
	return render(request, 'medicamento/medicamentoCreate.html', contexto)

def medicamentoEdit(request, cod_medicamento):
	medicamento = Medicamento.objects.get(pk=cod_medicamento)
	sistemas = SistemaMedicion.objects.all().order_by('nombre_sistema')
	if request.method == 'GET':
		contexto={'sistemas':sistemas, 'medicamento':medicamento}
	else:
		medicamento.nombre_medicamento=request.POST['nombre']
		medicamento.farmacia=request.POST['farmacia']
		medicamento.descripcion=request.POST['descripcion']
		medicamento.save()

		if not medicamento.sistema_medicion.exists():			
			for sis in sistemas:
				if 'sis_'+str(sis.cod_sistema) in request.POST:
					medicamento.sistema_medicion.add(sis)
					pass
				pass
			pass
		else:
			for sis in sistemas:
				if 'sis_'+str(sis.cod_sistema) in request.POST:
					if  not sis in medicamento.sistema_medicion.all():
						medicamento.sistema_medicion.add(sis)
						pass
					pass
				pass
			for sis in medicamento.sistema_medicion.all():
				if  not 'sis_'+str(sis.cod_sistema) in request.POST:
					medicamento.sistema_medicion.remove(sis)
					pass
				pass

		return redirect('hospital:medicamentoList')
	return render(request, 'medicamento/medicamentoCreate.html', contexto)

def sistemaMedicionList(request):
	if 'accion' in request.POST:
		accion = request.POST['accion']
		codigo_sistema = request.POST['sistema']
		sistema = SistemaMedicion.objects.get(cod_sistema = codigo_sistema)
		if accion == 'Eliminar':	
			sistema.delete()
			pass
		pass

	sistema = SistemaMedicion.objects.all().order_by('cod_sistema')
	contexto = {'sistemas':sistema}
	return render(request, 'sistemaMedicion/sistemaMedicionList.html', contexto)	

def sistemaMedicionCreate(request):
	if request.method == 'POST':
		sistema=SistemaMedicion()
		sistema.cod_sistema=request.POST['codigo']
		sistema.nombre_sistema=request.POST['nombre']
		sistema.save()
		pass
		return redirect('hospital:sistemaMedicionList')
	else:
		return render(request, 'sistemaMedicion/sistemaMedicionCreate.html')

def sistemaMedicionEdit(request, cod_sistema):
	sistema = SistemaMedicion.objects.get(pk=cod_sistema)
	if request.method == 'GET':
		contexto={'sistema':sistema}
	else:
		sistema.nombre_sistema=request.POST['nombre']
		sistema.save()
		return redirect('hospital:sistemaMedicionList')
	return render(request, 'sistemaMedicion/sistemaMedicionCreate.html', contexto)

def medicoList(request):
	if 'buscar' in request.GET:		
		if request.GET['buscarInput'] != "":
			palabraClave = request.GET['buscarInput']
			
			if Medico.objects.filter(cod_medico__contains = palabraClave).exists():
				medico = Medico.objects.filter(cod_medico__contains = palabraClave)
				contexto={'medicos':medico}
				return render(request, 'medico/medicoList.html', contexto)
			else:
				if Medico.objects.filter(especialidad__contains = palabraClave).exists():
					medico = Medico.objects.filter(especialidad__contains = palabraClave)
					contexto={'medicos':medico}
					return render(request, 'medico/medicoList.html', contexto)
				
		pass
	if 'accion' in request.POST:
		accion = request.POST['accion']
		codigo_medico = request.POST['medico']
		medico = Medico.objects.get(cod_medico = codigo_medico)
		if accion == 'Eliminar':	
			medico.delete()
			pass
						
		else:
			pass
		pass
	medico = Medico.objects.all().order_by('cod_medico')
	contexto = {'medicos':medico}
	return render(request, 'medico/medicoList.html', contexto)

def medicoCreate(request):
	especialidades=Especialidad.objects.all().order_by('nombre_especialidad')
	if request.method == 'POST':
		usuario=User()
		persona=Persona()
		medico=Medico()
		#usuario.is_staff=True
		usuario.first_name=request.POST['nombres']
		usuario.last_name=request.POST['apellidos']
		concac1=str(usuario.first_name).upper()
		concac1=concac1[0:3]
		concac2=str(usuario.last_name).upper()
		concac2=concac2[0:3]
		#Generar una cadena random
		stringRandom = str(random.randint(0,100))
		nombreUser = concac1 + concac2	
		usuario.username=nombreUser
		password=concac1+concac2+stringRandom
		usuario.set_password(password)
		usuario.save()
		persona.usuario=usuario
		persona.sexo=Sexo.objects.get(cod_sexo=str(request.POST['sexo']))
		persona.fecha_nacimiento=request.POST['fecha_nacimiento']
		persona.save()
		medico.cod_persona=persona
		medico.cod_medico=request.POST['cod_medico']
		medico.num_regsitro=request.POST['num_registro']
		medico.save()
		for esp in especialidades:
			if 'esp_'+esp.cod_especialidad in request.POST:
				medico.especialidad.add(esp)
				pass
			pass
		pass
		contexto = {'password':password,'username':nombreUser}
		return render(request, 'medico/medicoDetalle.html',contexto)
	else:
		contexto = {'especialidades':especialidades}
	return render(request, 'medico/medicoCreate.html',contexto)

def medicoEdit(request, cod_medico):
	medico = Medico.objects.get(pk=cod_medico)
	especialidades=Especialidad.objects.all().order_by('nombre_especialidad')
	if request.method == 'GET':
		fecha=str(medico.cod_persona.fecha_nacimiento)
		contexto = {'medico':medico,'especialidades':especialidades,'fecha':fecha}
	else:
		person=Persona.objects.get(pk=medico.cod_persona.pk)
		user=User.objects.get(pk=person.usuario.pk)

		user.first_name=request.POST['nombres']
		user.last_name=request.POST['apellidos']
		user.save()

		person.sexo=Sexo.objects.get(cod_sexo=str(request.POST['sexo']))
		person.fecha_nacimiento=request.POST['fecha_nacimiento']
		person.save()
		medico.num_regsitro=request.POST['num_registro']
		medico.save()

		if not medico.especialidad.exists():			
			for esp in especialidades:
				if 'esp_'+esp.cod_especialidad in request.POST:
					medico.especialidad.add(esp)
					pass
				pass
			pass
		else:
			for esp in especialidades:
				if 'esp_'+esp.cod_especialidad in request.POST:
					if  not esp in medico.especialidad.all():
						medico.especialidad.add(esp)
						pass
					pass
				pass
			for esp in medico.especialidad.all():
				if  not 'esp_'+esp.cod_especialidad in request.POST:
					medico.especialidad.remove(esp)
					pass
				pass
				
		return redirect('hospital:medicoList')
	return render(request, 'medico/medicoEdit.html', contexto)

def calcular_edad(fecha_nacimiento):
 
    edad = date.today().year - fecha_nacimiento.year
    cumpleanios = fecha_nacimiento + relativedelta(years=edad)
 
    if cumpleanios > date.today():
        edad = edad - 1
 
    return edad

def expedienteDetails(request, cod_paciente,tipoPersona):
	if request.method == 'GET':
		paciente = Paciente.objects.get(cod_paciente = cod_paciente)
		expediente = Expediente.objects.get(cod_paciente = paciente.id)
		cod_person = paciente.cod_persona.id
		persona = Persona.objects.get(id = cod_person)
		user = persona.usuario.id
		usuario = User.objects.get(id = user)
		edad = calcular_edad(persona.fecha_nacimiento)
		citas = Cita.objects.filter(paciente=paciente.id).order_by('-fecha_hora_cita')
		consultas = Consulta.objects.filter(num_expediente=expediente.id).order_by('-fecha_consulta')
		contexto = {'expediente':expediente,'paciente':paciente,'persona':persona, 'usuario':usuario,'edad':edad,'citas':citas,'consultas':consultas,'tipoPersona':str(tipoPersona)}
		return render(request, 'resepcionista/expedienteDetails.html',contexto)
		pass

def consultaDetails(request, cod_consulta,tipoPersona):
	if request.method == 'GET':
		consulta = Consulta.objects.get(cod_consulta=cod_consulta)
		recetas = ResetaMedica.objects.filter(cod_consulta = consulta.cod_consulta).order_by('-cod_consulta')
		contexto = {'consulta':consulta,'recetas':recetas,'tipoPersona':str(tipoPersona)}

		return render(request, 'resepcionista/consultaDetails.html',contexto)
		pass

#Final views Marco

#**************************************ROSA**************************************************************************

def resepcionistaList(request):
	if 'buscar' in request.GET:		
		if request.GET['buscarInput'] != "":
			palabraClave = request.GET['buscarInput']
			
			if Resepcionista.objects.filter(cod_resepcionista__contains = palabraClave).exists():
				recepcionista = Resepcionista.objects.filter(cod_resepcionista__contains = palabraClave)
				contexto={'recepcionistas':recepcionista}
				return render(request, 'resepcionista/resepcionistaList.html', contexto)
				
		pass
	if 'accion' in request.POST:
		accion = request.POST['accion']
		cod_resepcionista = request.POST['recepcionista']
		recepcionista = Resepcionista.objects.get(cod_resepcionista = cod_resepcionista)
		id_persona = recepcionista.cod_persona_id
		print(id_persona)
		persona = Persona.objects.get(id=id_persona)
		print(persona)
		id_usuario = persona.usuario_id
		print(id_usuario)
		usuario = User.objects.get(id=id_usuario)
		if accion == 'Eliminar':	
			recepcionista.delete()
			persona.delete()
			usuario.delete()
			pass
						
		else:
			pass
		pass
	recepcionista = Resepcionista.objects.all().order_by('cod_resepcionista')
	contexto = {'recepcionistas':recepcionista}
	return render(request, 'resepcionista/resepcionistaList.html', contexto)	

def resepcionistaCreate(request):
	sexo=Sexo.objects.all()
	nombres_sexos=request.POST.get('lista_sexo')
	if request.method == 'POST':
		usuario=User()
		persona=Persona()
		recepcionista=Resepcionista()
		#usuario.is_staff=True
		usuario.first_name=request.POST['nombres']
		usuario.last_name=request.POST['apellidos']
		concac1=str(usuario.first_name).upper()
		concac1=concac1[0:3]
		concac2=str(usuario.last_name).upper()
		concac2=concac2[0:3]
		#Generar una cadena random
		stringRandom = str(random.randint(0,100))
		nombreUser = concac1 + concac2	
		usuario.username=nombreUser
		print(usuario)
		password=concac1+concac2+stringRandom
		print(password)
		usuario.set_password(password)
		usuario.save()
		persona.usuario=usuario
		s=Sexo.objects.get(nombre_sexo=nombres_sexos)
		persona.sexo=s
		print(s)
		persona.fecha_nacimiento=request.POST['fecha_nacimiento']
		persona.save()
		recepcionista.cod_persona=persona
		recepcionista.cod_resepcionista=request.POST['cod_recepcionista']
		recepcionista.save()
		return redirect('hospital:resepcionistaList')
	return render(request, 'resepcionista/resepcionistaCreate.html', {'sexo':sexo})

def resepcionistaEdit(request, cod_resepcionista):
	resepcionista = Resepcionista.objects.get(pk=cod_resepcionista)
	sexo=Sexo.objects.all()
	nombres_sexos=request.POST.get('lista_sexo')
	if request.method == 'GET':
		fecha=str(resepcionista.cod_persona.fecha_nacimiento)
		contexto = {'resepcionista': resepcionista, 'sexo':sexo, 'fecha':fecha}
	else:
		person=Persona.objects.get(pk=resepcionista.cod_persona.pk)
		user=User.objects.get(pk=person.usuario.pk)
		user.first_name=request.POST['nombres']
		user.last_name=request.POST['apellidos']
		user.save()
		s=Sexo.objects.get(nombre_sexo=nombres_sexos)
		person.sexo=s
		person.fecha_nacimiento=request.POST['fecha_nacimiento']
		person.save()
		return redirect('hospital:resepcionistaList')
	return render(request, 'resepcionista/resepcionistaEdit.html',  contexto)

def atenderPacientesList(request):
	if 'buscar' in request.GET:		
		if request.GET['buscarInput'] != "":
			palabraClave = request.GET['buscarInput']
			
			if Paciente.objects.filter(cod_paciente__contains = palabraClave).exists():
				paciente = Paciente.objects.filter(cod_paciente__contains = palabraClave)
				contexto={'pacientes':paciente}
				return render(request, 'paciente/atenderPacienteList.html', contexto)
				
		pass
	if 'accion' in request.POST:
		accion = request.POST['accion']
		cod_paciente = request.POST['paciente']
		paciente = Paciente.objects.get(cod_paciente = cod_paciente)
		if accion == 'Eliminar':	
			paciente.delete()
			pass
						
		else:
			pass
		pass
	paciente = Paciente.objects.all().order_by('cod_paciente')
	contexto = {'pacientes':paciente}
	return render(request, 'paciente/atenderPacienteList.html', contexto)

def expedienteDetailsPaciente(request, cod_paciente,tipoPersona):
	if request.method == 'GET':
		paciente = Paciente.objects.get(cod_paciente = cod_paciente)
		expediente = Expediente.objects.get(cod_paciente = paciente.id)
		cod_person = paciente.cod_persona.id
		persona = Persona.objects.get(id = cod_person)
		user = persona.usuario.id
		usuario = User.objects.get(id = user)
		edad = calcular_edad(persona.fecha_nacimiento)
		citas = Cita.objects.filter(paciente=paciente.id).order_by('-fecha_hora_cita')
		consultas = Consulta.objects.filter(num_expediente=expediente.id).order_by('-fecha_consulta')
		contexto = {'expediente':expediente,'paciente':paciente,'persona':persona, 'usuario':usuario,'edad':edad,'citas':citas,'consultas':consultas,'tipoPersona':str(tipoPersona)}
		return render(request, 'paciente/expedienteDetails.html',contexto)
		pass

def consultaDetailsPaciente(request, cod_consulta,tipoPersona):
	if request.method == 'GET':
		consulta = Consulta.objects.get(cod_consulta=cod_consulta)
		recetas = ResetaMedica.objects.filter(cod_consulta = consulta.cod_consulta).order_by('-cod_consulta')
		contexto = {'consulta':consulta,'recetas':recetas,'tipoPersona':str(tipoPersona)}
		return render(request, 'paciente/consultaDetails.html',contexto)
		pass

def consultaCreate(request, cod_paciente):
	c=str(cod_paciente)
	contexto = {'c':cod_paciente}
	if request.method == 'POST':
		usuario=User()
		persona=Persona()
		medico=Medico()
		paciente=Paciente()
		expediente=Expediente()
		consulta=Consulta()
		consulta.cod_consulta=request.POST['cod_consulta']
		consulta.fecha_consulta=request.POST['fecha_consulta']
		consulta.diagnostico=request.POST['diagnostico']
		usuario_log=User.objects.get(username=request.user)
		persona=Persona.objects.get(usuario_id=usuario_log)
		medico=Medico.objects.get(cod_persona=persona)
		cod = medico.cod_medico
		consulta.cod_medico_id=cod
		paciente=Paciente.objects.get(cod_paciente=c)
		expediente=Expediente.objects.get(cod_paciente=paciente)
		ids=expediente.id
		consulta.num_expediente_id=ids
		consulta.save()
		return redirect('hospital:atenderPacientesList')
	return render(request, 'consulta/consultaCreate.html', contexto)

def recetaCreate(request, cod_consulta):
	medicamento=Medicamento.objects.all()
	nombre_medicamento=request.POST.get('lista_medicamento')
	consult=str(cod_consulta)
	contexto = {'consult':cod_consulta}
	if request.method == 'POST':
		consulta = Consulta()
		medicina = Medicamento()
		receta = ResetaMedica()
		consulta=Consulta.objects.get(cod_consulta=consult)
		receta.cod_consulta=consulta
		receta.cantidad=request.POST['cantidad']
		med=Medicamento.objects.get(nombre_medicamento=nombre_medicamento)
		receta.cod_medicamento=med
		receta.save()
		return redirect('hospital:atenderPacientesList')
	return render(request, 'receta/recetaCreate.html', {'medicamento':medicamento}, contexto)
	