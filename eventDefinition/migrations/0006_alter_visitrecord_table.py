# Generated by Django 3.2.10 on 2023-01-12 02:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventDefinition', '0005_alter_visitrecord_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='visitrecord',
            table='fVisitRecord',
        ),
    ]
