from django.urls import path, include
from .views import *

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("analitic", analitic, name="analitic"),
    path("barangmasuk", barangmasuk, name="barangmasuk"),
    path("tbdatabarang", tbdatabarang, name="tbdatabarang"),
    path("edititem/<int:id>", editBarangMasuk, name="edititem"),
    path("deleteitem/<int:id>", deleteBarangMasuk, name="deleteitem"),
    path("barangkeluar", barangkeluar, name="barangkeluar"),
    path("riwayatdata", tbriwayatdata, name="riwayatdata"),



]
