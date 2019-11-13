from django.db import models
from django.conf import settings


# Create your models here.
class Sexo(models.Model):
	cod_sexo=models.CharField(max_length=10,primary_key=True)
	nombre_sexo=models.CharField(max_length=8)
	def __str__(self):
		return self.nombre_sexo

class Persona(models.Model):
	usuario = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	sexo=models.ForeignKey(Sexo,on_delete=models.CASCADE)
	fecha_nacimiento=models.DateField(null=True)
	def __str__(self):
		return self.usuario.first_name

class Resepcionista(models.Model):
	cod_persona=models.ForeignKey(Persona,on_delete=models.CASCADE)
	cod_resepcionista=models.CharField(max_length=10,primary_key=True)
	def __str__(self):
		return self.cod_resepcionista

class Paciente(models.Model):
	cod_paciente=models.CharField(max_length=10,primary_key=True)
	cod_persona=models.ForeignKey(Persona,on_delete=models.CASCADE)
	def __str__(self):
		return self.cod_paciente

class Especialidad(models.Model):
	cod_especialidad=models.CharField(max_length=10,primary_key=True)
	nombre_especialidad=models.CharField(max_length=50)

class Medico(models.Model):
	especialidad=models.ForeignKey(Especialidad,on_delete=models.CASCADE)
	cod_persona=models.ForeignKey(Persona,on_delete=models.CASCADE)
	cod_medico=models.CharField(max_length=10,primary_key=True)
	num_regsitro=models.CharField(max_length=20)

class Expediente(models.Model):
	cod_resepcionista=models.CharField(max_length=10,primary_key=True)
	cod_paciente=models.OneToOneField(Paciente,on_delete=models.CASCADE)

class Consulta(models.Model):
	cod_consulta=models.CharField(max_length=10,primary_key=True)
	num_expediente=models.ForeignKey(Expediente,on_delete=models.CASCADE)
	cod_medico=models.ForeignKey(Medico,on_delete=models.CASCADE)
	fecha_consulta=models.DateField(null=True)
	diagnostico=models.CharField(max_length=200)

class SistemaMedicion(models.Model):
	cod_sistema=models.IntegerField(primary_key=True)
	nombre_sistema=models.CharField(max_length=40)

class Medicamento(models.Model):
	cod_sistema_medicion=models.ForeignKey(SistemaMedicion,on_delete=models.CASCADE)
	farmacia=models.CharField(max_length=50)
	descripcion=models.CharField(max_length=100)
	cod_medicamento=models.CharField(max_length=10,primary_key=True)

class ResetaMedica(models.Model):
	cod_reseta=models.CharField(max_length=10,primary_key=True)
	cod_consulta=models.ForeignKey(Consulta,on_delete=models.CASCADE)
	cod_medicamento=models.ForeignKey(Medicamento,on_delete=models.CASCADE)
	cantidad=models.IntegerField()





