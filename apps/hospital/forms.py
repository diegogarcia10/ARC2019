from django import forms
from apps.hospital.models import Especialidad, Medicamento, SistemaMedicion, Medico, Resepcionista, Consulta

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

class MedicamentoForm(forms.ModelForm):

    class Meta:
        model = Medicamento

        fields = [
            'cod_medicamento',
            'nombre_medicamento',
            'farmacia',
            'descripcion',
            'sistema_medicion',

        ]
        labels = {
            'cod_medicamento' : 'Código',
            'nombre_medicamento' : 'Nombre',
            'farmacia' : 'Farmacia',
            'descripcion' : 'Descripción',
            'sistema_medicion' : 'Sistemas de Medición',

        }

        widgets = {
            'cod_medicamento' : forms.TextInput(attrs={'class':'form-control','placeholder':'Escriba el Código del Medicamento'}),
            'nombre_medicamento' : forms.TextInput(attrs={'class':'form-control','placeholder':'Escriba el Nombre del Medicamento'}),
            'farmacia': forms.TextInput(attrs={'class':'form-control','placeholder':'Escriba la farmacia del Medicamento'}),
            'descripcion' : forms.Textarea(attrs={'rows':5, 'class':'form-control','placeholder':'Escriba la descripción del Medicamento'}),
            'sistema_medicion': forms.CheckboxSelectMultiple(),
                    }

class MedicamentoForm_2(forms.ModelForm):

    class Meta:
        model = Medicamento

        fields = [
            'cod_medicamento',
            'nombre_medicamento',
            'farmacia',
            'descripcion',
            'sistema_medicion',

        ]
        labels = {
            'cod_medicamento' : 'Código',
            'nombre_medicamento' : 'Nombre',
            'farmacia' : 'Farmacia',
            'descripcion' : 'Descripción',
            'sistema_medicion' : 'Sistemas de Medición',

        }

        widgets = {
            'cod_medicamento' : forms.TextInput(attrs={'class':'form-control','readonly':'readonly','placeholder':'Escriba el Código del Medicamento'}),
            'nombre_medicamento' : forms.TextInput(attrs={'class':'form-control','placeholder':'Escriba el Nombre del Medicamento'}),
            'farmacia': forms.TextInput(attrs={'class':'form-control','placeholder':'Escriba la farmacia del Medicamento'}),
            'descripcion' : forms.Textarea(attrs={'rows':5, 'class':'form-control','placeholder':'Escriba la descripción del Medicamento'}),
            'sistema_medicion': forms.CheckboxSelectMultiple(),
                    }

class SistemaMedicionForm(forms.ModelForm):

    class Meta:
        model = SistemaMedicion

        fields = [
            'cod_sistema',
            'nombre_sistema',

        ]
        labels = {
            'cod_sistema' : 'Código',
            'nombre_sistema' : 'Nombre',

        }

        widgets = {
            'cod_sistema' : forms.TextInput(attrs={'class':'form-control','placeholder':'Escriba el Código del Sistema de Medicion'}),
            'nombre_sistema' : forms.TextInput(attrs={'class':'form-control','placeholder':'Escriba el Nombre del Sistema de Medicion'}),
                    }

class SistemaMedicionForm_2(forms.ModelForm):

    class Meta:
        model = SistemaMedicion

        fields = [
            'cod_sistema',
            'nombre_sistema',

        ]
        labels = {
            'cod_sistema' : 'Código',
            'nombre_sistema' : 'Nombre',

        }

        widgets = {
            'cod_sistema' : forms.TextInput(attrs={'class':'form-control','readonly':'readonly','placeholder':'Escriba el Código del Sistema de Medicion'}),
            'nombre_sistema' : forms.TextInput(attrs={'class':'form-control','placeholder':'Escriba el Nombre del Sistema de Medicion'}),
                    }

class MedicoForm(forms.ModelForm):

    class Meta:
        model = Medico

        fields = [
            'cod_medico',
            'num_regsitro',
            'especialidad',
            'cod_persona',

        ]
        labels = {
            'cod_medico' : 'Código',            
            'num_regsitro' : 'Número de Registro',
            'especialidad' : 'Especialidades',
            'cod_persona' : 'Persona',

        }

        widgets = {
            'cod_medico' : forms.TextInput(attrs={'class':'form-control','placeholder':'Escriba el Código del Medico'}),
            'num_regsitro' : forms.TextInput(attrs={'class':'form-control','placeholder':'Escriba el Numero de Registro del Medico'}),
            'especialidad': forms.CheckboxSelectMultiple(),
            'cod_persona': forms.Select(attrs={'class':'form-control'}),
                    }

class MedicoForm_2(forms.ModelForm):

    class Meta:
        model = Medico

        fields = [
            'cod_medico',
            'num_regsitro',
            'especialidad',
            'cod_persona',

        ]
        labels = {
            'cod_medico' : 'Código',
            'num_regsitro' : 'Numero de Registro',
            'especialidad' : 'Especialidades',
            'cod_persona' : 'Persona',

        }

        widgets = {
            'cod_medico' : forms.TextInput(attrs={'class':'form-control','readonly':'readonly','placeholder':'Escriba el Código del Medico'}),
            'num_regsitro' : forms.TextInput(attrs={'class':'form-control','placeholder':'Escriba el Numero de Registro del Medico'}),
            'especialidad': forms.CheckboxSelectMultiple(),
            'cod_persona': forms.Select(attrs={'class':'form-control'}),
                    }

