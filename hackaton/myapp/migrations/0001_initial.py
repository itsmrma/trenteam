# Generated by Django 5.0.4 on 2025-02-20 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('pdf_path', models.CharField(max_length=1000)),
                ('parole_chiave', models.CharField(max_length=1000)),
                ('file_url', models.CharField(max_length=1000)),
            ],
        ),
    ]
