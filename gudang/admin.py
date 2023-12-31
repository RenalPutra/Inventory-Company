from django.contrib import admin
from .models import *

# Register your models here.


class KategoriAdmin(admin.ModelAdmin):
    list_display = ['kategori']
    list_filter = ('kategori',)


class LokasiAdmin(admin.ModelAdmin):
    list_display = ['lokasi']
    list_filter = ('lokasi',)


class BarangMasukAdmin(admin.ModelAdmin):
    list_display = ['date', 'device', 'user', 'lokasi', 'pc', 'os', 'cpu',
                    'vga', 'ram', 'model', 'serialnumber', 'description', 'kategori', 'lokasi',]
    list_filter = ('date', 'device', 'user', 'lokasi', 'pc', 'os', 'cpu',
                   'vga', 'ram', 'model', 'serialnumber', 'description', 'kategori', 'lokasi',)


class BarangKeluarAdmin(admin.ModelAdmin):
    list_display = ['date_keluar', 'date_masuk', 'device', 'user', 'pc', 'os', 'cpu',
                    'vga', 'ram', 'model', 'serialnumber', 'description', 'kategori', 'lokasi',]
    list_filter = ('date_keluar', 'date_masuk', 'device', 'user', 'pc', 'os', 'cpu',
                   'vga', 'ram', 'model', 'serialnumber', 'description', 'kategori', 'lokasi',)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'is_read', 'timestamp']
    list_filter = ('title', 'content', 'is_read', 'timestamp')


admin.site.register(Kategori, KategoriAdmin)
admin.site.register(BarangMasuk, BarangMasukAdmin)
admin.site.register(BarangKeluar, BarangKeluarAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Lokasi, LokasiAdmin)
