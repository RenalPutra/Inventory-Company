# Generated by Django 3.2 on 2023-08-13 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gudang', '0003_alter_barangmasuk_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barangmasuk',
            name='cpu',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='barangmasuk',
            name='description',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='barangmasuk',
            name='device',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='barangmasuk',
            name='email',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='barangmasuk',
            name='model',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='barangmasuk',
            name='os',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='barangmasuk',
            name='pc',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='barangmasuk',
            name='ram',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='barangmasuk',
            name='serialnumber',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='barangmasuk',
            name='user',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='barangmasuk',
            name='vga',
            field=models.TextField(max_length=100),
        ),
    ]
