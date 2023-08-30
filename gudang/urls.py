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
    path("delete_selected", delete_selected, name="delete_selected"),
    path("fetch_notifications", fetch_notifications, name="fetch_notifications"),
    path("mark_notifications_as_read", mark_notifications_as_read,
         name="mark_notifications_as_read"),
    path("get_unread_notification_count", get_unread_notification_count,
         name="get_unread_notification_count"),
    path("delete_all_notifications", delete_all_notifications,
         name="delete_all_notifications"),




]
