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
    date = models.DateTimeField(auto_now_add=True)
    device = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    pc = models.CharField(max_length=100)
    os = models.CharField(max_length=100)
    cpu = models.CharField(max_length=100)
    vga = models.CharField(max_length=100)
    ram = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serialnumber = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)

    def __str__(self):
        return self.device + " - " + self.user + " - " + self.email + " - " + self.pc + " - " + self.os + " - " + self.cpu + " - " + self.vga + " - " + self.ram + " - " + self.model + " - " + self.serialnumber + " - " + self.description + " - " + str(self.kategori)


