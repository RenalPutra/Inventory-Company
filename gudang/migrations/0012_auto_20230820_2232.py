# Generated by Django 3.2 on 2023-08-20 14:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gudang', '0011_remove_barangkeluar_date_barangkeluar_date_keluar_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='barangkeluar',
            name='nama',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='barangmasuk',
            name='nama',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
