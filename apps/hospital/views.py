from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from apps.hospital.models import *
from apps.hospital.forms import *
#Librerias Necesarias para la comunicacion con el arduino
import time
import serial
import serial.tools.list_ports

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
		return render(request,'base/index.html',{'tipoPersona':tipoPersona})
	if id_tipo=="2":
		tipoPersona="2"
		print("Elijio 2")
		return render(request,'base/index.html',{'tipoPersona':tipoPersona})
	if id_tipo=="3":
		tipoPersona="3"
		print("Elijio 3")
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
#--------FIN PARTE DE DIEGO--------------#
#view Marco
def especialidadList(request):
	if 'buscar' in request.GET:		
		if request.GET['buscarInput'] != "":
			palabraClave = request.GET['buscarInput']
			
			if Especialidad.objects.filter(cod_especialidad__contains = palabraClave).exists():
				especialidad = Especialidad.objects.filter(cod_especialidad__contains = palabraClave)
				contexto={'especialidades':especialidad}
				return render(request, 'especialidad/especialidadList.html', contexto)
			else:
				if Especialidad.objects.filter(nombre_especialidad__contains = palabraClave).exists():
					especialidad = Especialidad.objects.filter(nombre_especialidad__contains = palabraClave)
					contexto={'especialidades':especialidad}
					return render(request, 'especialidad/especialidadList.html', contexto)
				
		pass
	if 'accion' in request.POST:
		accion = request.POST['accion']
		codigo_especialidad = request.POST['especialidad']
		especialidad = Especialidad.objects.get(cod_especialidad = codigo_especialidad)
		if accion == 'Eliminar':	
			especialidad.delete()
			pass
						
		else:
			pass
		pass
	especialidad = Especialidad.objects.all().order_by('cod_especialidad')
	contexto = {'especialidades':especialidad}
	return render(request, 'especialidad/especialidadList.html', contexto)	

def especialidadCreate(request):
	if request.method == 'POST':
		form = EspecialidadForm(request.POST)
		if form.is_valid():
			form.save()
			pass
		pass
		return redirect('hospital:especialidadList')
	else:
		form = EspecialidadForm()
	return render(request, 'especialidad/especialidadCreate.html', {'form':form})

def especialidadEdit(request, cod_especialidad):
	especialidad = Especialidad.objects.get(pk=cod_especialidad)
	if request.method == 'GET':
		form1 = EspecialidadForm_2(instance=especialidad)
	else:
		form1 = EspecialidadForm_2(request.POST, instance=especialidad)
		if form1.is_valid():
			form1.save()
		return redirect('hospital:especialidadList')
	return render(request, 'especialidad/especialidadCreate.html', {'form1':form1})

def medicamentoList(request):
	if 'buscar' in request.GET:		
		if request.GET['buscarInput'] != "":
			palabraClave = request.GET['buscarInput']
			
			if Medicamento.objects.filter(cod_medicamento__contains = palabraClave).exists():
				medicamento = Medicamento.objects.filter(cod_medicamento__contains = palabraClave)
				contexto={'medicamentos':medicamento}
				return render(request, 'medicamento/medicamentoList.html', contexto)
			else:
				if Medicamento.objects.filter(nombre_medicamento__contains = palabraClave).exists():
					medicamento = Medicamento.objects.filter(nombre_medicamento__contains = palabraClave)
					contexto={'medicamentos':medicamento}
					return render(request, 'medicamento/medicamentoList.html', contexto)
				
		pass
	if 'accion' in request.POST:
		accion = request.POST['accion']
		codigo_medicamento = request.POST['medicamento']
		medicamento = Medicamento.objects.get(cod_medicamento = codigo_medicamento)
		if accion == 'Eliminar':	
			medicamento.delete()
			pass
						
		else:
			pass
		pass
	medicamento = Medicamento.objects.all().order_by('cod_medicamento')
	contexto = {'medicamentos':medicamento}
	return render(request, 'medicamento/medicamentoList.html', contexto)

def medicamentoCreate(request):
	if request.method == 'POST':
		form = MedicamentoForm(request.POST)
		if form.is_valid():
			form.save()
			pass
		pass
		return redirect('hospital:medicamentoList')
	else:
		form = MedicamentoForm()
	return render(request, 'medicamento/medicamentoCreate.html', {'form':form})

def medicamentoEdit(request, cod_medicamento):
	medicamento = Medicamento.objects.get(pk=cod_medicamento)
	if request.method == 'GET':
		form1 = MedicamentoForm_2(instance=medicamento)
	else:
		form1 = MedicamentoForm_2(request.POST, instance=medicamento)
		if form1.is_valid():
			form1.save()
		return redirect('hospital:medicamentoList')
	return render(request, 'medicamento/medicamentoCreate.html', {'form1':form1})

def sistemaMedicionList(request):
	if 'buscar' in request.GET:		
		if request.GET['buscarInput'] != "":
			palabraClave = request.GET['buscarInput']
			
			if SistemaMedicion.objects.filter(cod_sistema__contains = palabraClave).exists():
				sistema = SistemaMedicion.objects.filter(cod_sistema__contains = palabraClave)
				contexto={'sistemas':sistema}
				return render(request, 'sistemaMedicion/sistemaMedicionList.html', contexto)
			else:
				if SistemaMedicion.objects.filter(nombre_sistema__contains = palabraClave).exists():
					sistema = SistemaMedicion.objects.filter(nombre_sistema__contains = palabraClave)
					contexto={'sistemas':sistema}
					return render(request, 'sistemaMedicion/sistemaMedicionList.html', contexto)
				
		pass
	if 'accion' in request.POST:
		accion = request.POST['accion']
		codigo_sistema = request.POST['sistema']
		sistema = SistemaMedicion.objects.get(cod_sistema = codigo_sistema)
		if accion == 'Eliminar':	
			sistema.delete()
			pass
						
		else:
			pass
		pass
	sistema = SistemaMedicion.objects.all().order_by('cod_sistema')
	contexto = {'sistemas':sistema}
	return render(request, 'sistemaMedicion/sistemaMedicionList.html', contexto)	

def sistemaMedicionCreate(request):
	if request.method == 'POST':
		form = SistemaMedicionForm(request.POST)
		if form.is_valid():
			form.save()
			pass
		pass
		return redirect('hospital:sistemaMedicionList')
	else:
		form = SistemaMedicionForm()
	return render(request, 'sistemaMedicion/sistemaMedicionCreate.html', {'form':form})

def sistemaMedicionEdit(request, cod_sistema):
	sistema = SistemaMedicion.objects.get(pk=cod_sistema)
	if request.method == 'GET':
		form1 = SistemaMedicionForm_2(instance=sistema)
	else:
		form1 = SistemaMedicionForm_2(request.POST, instance=sistema)
		if form1.is_valid():
			form1.save()
		return redirect('hospital:sistemaMedicionList')
	return render(request, 'sistemaMedicion/sistemaMedicionCreate.html', {'form1':form1})

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
	if request.method == 'POST':
		form = MedicoForm(request.POST)
		if form.is_valid():
			form.save()
			pass
		pass
		return redirect('hospital:medicoList')
	else:
		form = MedicoForm()
	return render(request, 'medico/medicoCreate.html', {'form':form})

def medicoEdit(request, cod_medico):
	medico = Medico.objects.get(pk=cod_medico)
	if request.method == 'GET':
		form1 = MedicoForm_2(instance=medico)
	else:
		form1 = MedicoForm_2(request.POST, instance=medico)
		if form1.is_valid():
			form1.save()
		return redirect('hospital:medicoList')
	return render(request, 'medico/medicoCreate.html', {'form1':form1})
#Final views Marco

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
		if accion == 'Eliminar':	
			recepcionista.delete()
			pass
						
		else:
			pass
		pass
	recepcionista = Resepcionista.objects.all().order_by('cod_resepcionista')
	contexto = {'recepcionistas':recepcionista}
	return render(request, 'resepcionista/resepcionistaList.html', contexto)	

def resepcionistaCreate(request):
	if request.method == 'POST':
		form = ResepcionistaForm(request.POST)
		if form.is_valid():
			form.save()
			pass
		pass
		return redirect('hospital:resepcionistaList')
	else:
		form = ResepcionistaForm()
	return render(request, 'resepcionista/resepcionistaCreate.html', {'form':form})

def resepcionistaEdit(request, cod_resepcionista):
	recepcionista = Resepcionista.objects.get(pk=cod_resepcionista)
	if request.method == 'GET':
		form1 = ResepcionistaForm_2(instance=recepcionista)
	else:
		form1 = ResepcionistaForm_2(request.POST, instance=recepcionista)
		if form1.is_valid():
			form1.save()
		return redirect('hospital:resepcionistaList')
	return render(request, 'resepcionista/resepcionistaCreate.html', {'form1':form1})