# Generated by Django 5.1.2 on 2024-10-24 02:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bankapp', '0005_bankaccount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='birthdate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='cnpj',
            field=models.CharField(blank=True, max_length=14, null=True, unique=True, validators=[django.core.validators.RegexValidator('^\\d{14}$')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='cpf',
            field=models.CharField(blank=True, max_length=11, null=True, unique=True, validators=[django.core.validators.RegexValidator('^\\d{11}$')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='creation_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
