from django.urls import path, include
from .views import *

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("barangmasuk", barangmasuk, name="barangmasuk"),
    path("tbdatabarang", tbdatabarang, name="tbdatabarang"),


]
