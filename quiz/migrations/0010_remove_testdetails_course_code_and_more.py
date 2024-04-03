# Generated by Django 4.2.7 on 2023-11-14 06:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0003_auto_20231111_1457'),
        ('quiz', '0009_testdetails_remove_course_question_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testdetails',
            name='course_code',
        ),
        migrations.AddField(
            model_name='testdetails',
            name='teacher_id',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='teacher.teacher'),
            preserve_default=False,
        ),
    ]
