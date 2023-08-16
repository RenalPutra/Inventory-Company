from django.db import models

# Create your models here.

# buat databse sesuai dengan form input


class Kategori(models.Model):
    kategori = models.CharField(max_length=100)

    def __str__(self):
        return self.kategori

    class Meta:
        verbose_name_plural = "kategori"


class BarangMasuk(models.Model):
    date = models.CharField(max_length=100)
    device = models.TextField(max_length=100)
    user = models.TextField(max_length=100)
    email = models.TextField(max_length=100)
    pc = models.TextField(max_length=100)
    os = models.TextField(max_length=100)
    cpu = models.TextField(max_length=100)
    vga = models.TextField(max_length=100)
    ram = models.TextField(max_length=100)
    model = models.TextField(max_length=100)
    serialnumber = models.TextField(max_length=100)
    description = models.TextField(max_length=100)
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)

    def __str__(self):
        return self.device + ' - ' + self.user

    class Meta:
        verbose_name_plural = "barang masuk"


class BarangKeluar(models.Model):
    date_keluar = models.CharField(max_length=100,blank=True, null=True)
    date_masuk = models.CharField(max_length=100,blank=True, null=True)
    device = models.TextField(max_length=100)
    user = models.TextField(max_length=100)
    email = models.TextField(max_length=100)
    pc = models.TextField(max_length=100)
    os = models.TextField(max_length=100)
    cpu = models.TextField(max_length=100)
    vga = models.TextField(max_length=100)
    ram = models.TextField(max_length=100)
    model = models.TextField(max_length=100)
    serialnumber = models.TextField(max_length=100)
    description = models.TextField(max_length=100)
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)

    def __str__(self):
        return self.device + ' - ' + self.user

    class Meta:
        verbose_name_plural = "barang keluar"
