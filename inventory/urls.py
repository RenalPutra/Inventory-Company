from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", welcome, name="welcome"),
    path("dashboard/", include("gudang.urls")),

]
