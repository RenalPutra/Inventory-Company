# Generated by Django 3.2 on 2023-08-13 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gudang', '0005_barangkeluar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barangmasuk',
            name='kategori',
            field=models.TextField(max_length=100),
        ),
    ]
