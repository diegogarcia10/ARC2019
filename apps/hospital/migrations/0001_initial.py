# Generated by Django 2.0.5 on 2019-12-12 16:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora_cita', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('cod_consulta', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('fecha_consulta', models.DateField(null=True)),
                ('diagnostico', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Especialidad',
            fields=[
                ('cod_especialidad', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombre_especialidad', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Expediente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Medicamento',
            fields=[
                ('nombre_medicamento', models.CharField(max_length=40)),
                ('farmacia', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=100)),
                ('cod_medicamento', models.CharField(max_length=10, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Medico',
            fields=[
                ('cod_medico', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('num_regsitro', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_paciente', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_nacimiento', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Resepcionista',
            fields=[
                ('cod_resepcionista', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('cod_persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.Persona')),
            ],
        ),
        migrations.CreateModel(
            name='ResetaMedica',
            fields=[
                ('cod_reseta', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField()),
                ('cod_consulta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.Consulta')),
                ('cod_medicamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.Medicamento')),
            ],
        ),
        migrations.CreateModel(
            name='Sexo',
            fields=[
                ('cod_sexo', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombre_sexo', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='SistemaMedicion',
            fields=[
                ('cod_sistema', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre_sistema', models.CharField(max_length=40)),
            ],
        ),
        migrations.AddField(
            model_name='persona',
            name='sexo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.Sexo'),
        ),
        migrations.AddField(
            model_name='persona',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='paciente',
            name='cod_persona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.Persona'),
        ),
        migrations.AddField(
            model_name='medico',
            name='cod_persona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.Persona'),
        ),
        migrations.AddField(
            model_name='medico',
            name='especialidad',
            field=models.ManyToManyField(to='hospital.Especialidad'),
        ),
        migrations.AddField(
            model_name='medicamento',
            name='sistema_medicion',
            field=models.ManyToManyField(to='hospital.SistemaMedicion'),
        ),
        migrations.AddField(
            model_name='expediente',
            name='cod_paciente',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='hospital.Paciente'),
        ),
        migrations.AddField(
            model_name='consulta',
            name='cod_medico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.Medico'),
        ),
        migrations.AddField(
            model_name='consulta',
            name='num_expediente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.Expediente'),
        ),
        migrations.AddField(
            model_name='cita',
            name='medico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.Medico'),
        ),
        migrations.AddField(
            model_name='cita',
            name='paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.Paciente'),
        ),
    ]
