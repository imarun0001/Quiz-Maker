# Generated by Django 4.2.7 on 2023-11-26 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0006_alter_teacher_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='country_code',
            field=models.CharField(default=91, max_length=5),
            preserve_default=False,
        ),
    ]
