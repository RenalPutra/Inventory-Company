# Generated by Django 3.2 on 2023-08-13 13:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gudang', '0006_alter_barangmasuk_kategori'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barangmasuk',
            name='kategori',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gudang.kategori'),
        ),
    ]
