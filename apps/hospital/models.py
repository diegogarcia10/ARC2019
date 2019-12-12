from django.db import models
from django.conf import settings


# Create your models here.
class Sexo(models.Model):
	cod_sexo=models.CharField(max_length=10,primary_key=True)
	nombre_sexo=models.CharField(max_length=10)
	def __str__(self):
		return str(self.nombre_sexo)

class Persona(models.Model):
	usuario = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	sexo=models.ForeignKey(Sexo,on_delete=models.CASCADE)
	fecha_nacimiento=models.DateField(null=True)
	def __str__(self):
		return str(self.usuario)

class Resepcionista(models.Model):
	cod_persona=models.ForeignKey(Persona,on_delete=models.CASCADE)
	cod_resepcionista=models.CharField(max_length=10,primary_key=True)
	def __str__(self):
		return str(self.cod_persona)

class Paciente(models.Model):
	cod_paciente=models.CharField(max_length=15)
	cod_persona=models.ForeignKey(Persona,on_delete=models.CASCADE)
	def __str__(self):
		return str(self.cod_persona)

class Especialidad(models.Model):
	cod_especialidad=models.CharField(max_length=10,primary_key=True)
	nombre_especialidad=models.CharField(max_length=50)
	def __str__(self):
		return str(self.nombre_especialidad)

class Medico(models.Model):
	especialidad=models.ManyToManyField(Especialidad)
	cod_persona=models.ForeignKey(Persona,on_delete=models.CASCADE)
	cod_medico=models.CharField(max_length=10,primary_key=True)
	num_regsitro=models.CharField(max_length=20)
	def __str__(self):
		return str(self.num_regsitro)

class Expediente(models.Model):
	cod_paciente=models.OneToOneField(Paciente,on_delete=models.CASCADE)
	def __str__(self):
		return str(self.cod_paciente)

class Consulta(models.Model):
	cod_consulta=models.CharField(max_length=10,primary_key=True)
	num_expediente=models.ForeignKey(Expediente,on_delete=models.CASCADE)
	cod_medico=models.ForeignKey(Medico,on_delete=models.CASCADE)
	fecha_consulta=models.DateField(null=True)
	diagnostico=models.CharField(max_length=200)
	def __str__(self):
		return str(self.cod_consulta)

class SistemaMedicion(models.Model):
	cod_sistema=models.IntegerField(primary_key=True)
	nombre_sistema=models.CharField(max_length=40)
	def __str__(self):
		return str(self.nombre_sistema)

class Medicamento(models.Model):
	sistema_medicion=models.ManyToManyField(SistemaMedicion)
	nombre_medicamento=models.CharField(max_length=40)
	farmacia=models.CharField(max_length=50)
	descripcion=models.CharField(max_length=100)
	cod_medicamento=models.CharField(max_length=10,primary_key=True)
	def __str__(self):
		return str(self.farmacia)

class ResetaMedica(models.Model):
	cod_reseta=models.CharField(max_length=10,primary_key=True)
	cod_consulta=models.ForeignKey(Consulta,on_delete=models.CASCADE)
	cod_medicamento=models.ForeignKey(Medicamento,on_delete=models.CASCADE)
	cantidad=models.IntegerField()
	def __str__(self):
		return str(self.cod_reseta)

class Cita(models.Model):
	medico=models.ForeignKey(Medico,on_delete=models.CASCADE)
	paciente=models.ForeignKey(Paciente,on_delete=models.CASCADE)
	fecha_hora_cita=models. DateTimeField()
