from django.contrib import admin
from .models import *

# Register your models here.


class KategoriAdmin(admin.ModelAdmin):
    list_display = ['kategori']
    list_filter = ('kategori',)


class BarangMasukAdmin(admin.ModelAdmin):
    list_display = ['date', 'device', 'user', 'email', 'pc', 'os', 'cpu',
                    'vga', 'ram', 'model', 'serialnumber', 'description', 'kategori',]
    list_filter = ('date', 'device', 'user', 'email', 'pc', 'os', 'cpu',
                   'vga', 'ram', 'model', 'serialnumber', 'description', 'kategori',)


admin.site.register(Kategori, KategoriAdmin)
admin.site.register(BarangMasuk, BarangMasukAdmin)
