# Generated by Django 3.2.10 on 2022-01-03 03:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('escuela', '0002_periodoescolar_periodo_activo'),
        ('personas', '0006_alter_estudiante_seccion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estudiante',
            name='grado_matriculado',
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='escuela_previa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='escuela.escuela'),
        ),
    ]