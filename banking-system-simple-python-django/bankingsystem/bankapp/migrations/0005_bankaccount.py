# Generated by Django 5.1.2 on 2024-10-24 01:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bankapp', '0004_alter_userprofile_cnpj_alter_userprofile_cpf_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agency', models.CharField(default='0001', max_length=4, null=True)),
                ('number', models.CharField(max_length=10, null=True, unique=True)),
                ('account_type', models.CharField(choices=[('person', 'Person'), ('legal_entity', 'Legal Entity')], max_length=20, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bankapp.userprofile')),
            ],
        ),
    ]
