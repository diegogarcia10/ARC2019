from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from apps.hospital.models import *
from apps.hospital.forms import *

def usuarioActual(param=None):
	usuario_actual=""
	if param==None:
		usuario_actual=""
	else:
		usuario_actual=param
	return usuario_actual

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
#Final views Marco