# Generated by Django 4.2.4 on 2023-09-08 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("gudang", "0015_barangkeluar_lokasi_barangmasuk_lokasi"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="barangkeluar",
            name="email",
        ),
        migrations.RemoveField(
            model_name="barangmasuk",
            name="email",
        ),
    ]
