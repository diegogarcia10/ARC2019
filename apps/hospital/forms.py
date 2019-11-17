from django import forms
from apps.hospital.models import Especialidad

class EspecialidadForm(forms.ModelForm):

    class Meta:
        model = Especialidad

        fields = [
            'cod_especialidad',
            'nombre_especialidad',

        ]
        labels = {
            'cod_especialidad' : 'Código',
            'nombre_especialidad' : 'Nombre',

        }

        widgets = {
            'cod_especialidad' : forms.TextInput(attrs={'class':'form-control','placeholder':'Escriba el Código de la Especialidad'}),
            'nombre_especialidad' : forms.TextInput(attrs={'class':'form-control','placeholder':'Escriba el Nombre de la Especialidad'}),
                    }

class EspecialidadForm_2(forms.ModelForm):

    class Meta:
        model = Especialidad

        fields = [
            'cod_especialidad',
            'nombre_especialidad',

        ]
        labels = {
            'cod_especialidad' : 'Código',
            'nombre_especialidad' : 'Nombre',

        }

        widgets = {
            'cod_especialidad' : forms.TextInput(attrs={'class':'form-control','readonly':'readonly','placeholder':'Escriba el Código de la Especialidad'}),
            'nombre_especialidad' : forms.TextInput(attrs={'class':'form-control','placeholder':'Escriba el Nombre de la Especialidad'}),
                    }