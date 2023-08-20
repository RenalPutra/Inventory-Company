from django.urls import path, include
from .views import *

urlpatterns = [
    path("", analitic, name="analitic"),
    path("barangmasuk", barangmasuk, name="barangmasuk"),
    path("tbdatabarang", tbdatabarang, name="tbdatabarang"),
    path("edititem/<int:id>", editBarangMasuk, name="edititem"),
    path("deleteitem/<int:id>", deleteBarangMasuk, name="deleteitem"),
    path("deleteitemkeluar/<int:id>", deleteBarangKeluar, name="deleteitemkeluar"),
    path("barangkeluar", barangkeluar, name="barangkeluar"),
    path("riwayatdata", tbriwayatdata, name="riwayatdata"),
    path("login", login, name="login"),
    path("register", register, name="register"),
    path("logout", logout_view, name="logout"),
    path("usertb", tbuser, name="usertb"),
    path("edituser/<int:id>", editUser, name="edituser"),
    path("hapususer/<int:id>", hapusUsers, name="hapususer"),
    path("export-to-csv", export_to_csv, name="exportcsv"),




]
