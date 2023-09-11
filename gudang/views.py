import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Kategori, BarangKeluar
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth import login as auth_login, authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.db.models import Q
from django.db import transaction
from django.http import HttpResponse
from .models import *
from datetime import datetime
from inventory import views
import csv
# Create your views here.


def is_operator(user):
    if user.groups.filter(name="Operator").exists():
        return True
    else:
        return False


@login_required
def analitic(request):
    template_name = "analitic.html"

    if request.user.groups.filter(name="Operator").exists():
        request.session['is_operator'] = 'operator'

    # Menghitung total data masuk dan data keluar
    total_data_masuk = BarangMasuk.objects.count()
    total_data_keluar = BarangKeluar.objects.count()

    # Mengambil 5 recent activity data masuk dan data keluar terbaru
    recent_activity_masuk = BarangMasuk.objects.order_by('-date')[:5]
    recent_activity_keluar = BarangKeluar.objects.order_by('-date_keluar')[:5]

    # Mengumpulkan data recent activity untuk ditampilkan di template
    recent_activity = []
    for activity in recent_activity_masuk:
        recent_activity.append({
            'nama': activity.nama,
            'device': activity.device,  # 'device' adalah nama field di model 'BarangMasuk
            'name': activity.user,
            'lokasi': activity.lokasi,
            'joined': activity.date,
            'type': 'Data Masuk',
            'status': 'Ok'  # Anda dapat mengganti ini sesuai dengan kebutuhan
        })
    for activity in recent_activity_keluar:
        recent_activity.append({
            'nama': activity.nama,
            'device': activity.device,  # 'device' adalah nama field di model 'BarangKeluar
            'name': activity.user,
            'lokasi': activity.lokasi,
            'joined': activity.date_keluar,
            'type': 'Data Keluar',
            'status': 'Ok'  # Anda dapat mengganti ini sesuai dengan kebutuhan
        })

    context = {
        'total_data_masuk': total_data_masuk,
        'total_data_keluar': total_data_keluar,
        'count_new_recent_activity': len(recent_activity),
        'recent_activity': recent_activity,
    }

    return render(request, template_name, context)


@login_required
def dashboard(request):
    template_name = "base.html"
    user = User.objects.all()
    context = {
        'user': user,
    }
    return render(request, template_name, context)


@login_required
def barangmasuk(request):
    template_name = "formbarangmasuk.html"
    kategori = Kategori.objects.all()
    lokasi = Lokasi.objects.all()
    waktu_sekarang = datetime.now()
    format_tanggal = waktu_sekarang.strftime("%a %m %Y - %H:%M:%S")
    if request.method == 'POST':
        device = request.POST.get('device')
        user = request.POST.get('user')
        lokasi = request.POST.get('lokasi')
        pc = request.POST.get('pc')
        os = request.POST.get('os')
        cpu = request.POST.get('cpu')
        vga = request.POST.get('vga')
        ram = request.POST.get('ram')
        model = request.POST.get('model')
        serialnumber = request.POST.get('serialnumber')
        description = request.POST.get('description')
        kategori = request.POST.get('kategori')
        penulis = request.user
        # jika data kategori tidak ada maka akan muncul pesan error

        if not kategori:
            messages.error(
                request, 'Kategori tidak boleh kosong')
            return redirect('barangmasuk')
        else:
            kat = Kategori.objects.get(kategori=kategori)
            lok = Lokasi.objects.get(lokasi=lokasi)
            barang_masuk_data = BarangMasuk.objects.create(
                date=format_tanggal,
                device=device,
                user=user,
                lokasi=lok,
                pc=pc,
                os=os,
                cpu=cpu,
                vga=vga,
                ram=ram,
                model=model,
                serialnumber=serialnumber,
                description=description,
                kategori=kat,
                nama=penulis
            )
            # Buat notifikasi
            title = "Barang Masuk"
            content = f"Barang {barang_masuk_data.device} telah masuk pada tanggal {barang_masuk_data.date}."
            Notification.objects.create(title=title, content=content)

            messages.success(
                request, 'Data berhasil disimpan')
            return redirect('barangmasuk')

    context = {
        'kategori': kategori,
        'lokasi': lokasi,
    }

    return render(request, template_name, context)

# jika barang keluar user hanya perlu mengisi Device saja
# dan data lainnya akan otomatis terisi
# jika device tidak ada maka akan muncul pesan error


@login_required
def barangkeluar(request):
    template_name = "formbarangkeluar.html"
    kategori = Kategori.objects.all()
    lokasi = Lokasi.objects.all()
    barangmasuk = BarangMasuk.objects.all()
    waktu_sekarang = datetime.now()
    penulis = request.user
    format_tanggal = waktu_sekarang.strftime("%a %m %Y - %H:%M:%S")
    if request.method == 'POST':
        device = request.POST.get('device')
        user = request.POST.get('user')
        existing_barang = BarangMasuk.objects.filter(device=device).first()
        if existing_barang:
            if 'submit_form' in request.POST:
                # Jika tombol "Submit" ditekan, simpan data ke BarangKeluar
                form_data = {
                    'date_keluar': format_tanggal,
                    'date_masuk': existing_barang.date,
                    'device': existing_barang.device,
                    'user': existing_barang.user,
                    'lokasi': existing_barang.lokasi,
                    'pc': existing_barang.pc,
                    'os': existing_barang.os,
                    'cpu': existing_barang.cpu,
                    'vga': existing_barang.vga,
                    'ram': existing_barang.ram,
                    'model': existing_barang.model,
                    'serialnumber': existing_barang.serialnumber,
                    'description': existing_barang.description,
                    'kategori': existing_barang.kategori.kategori,
                    'nama': penulis
                }
                kat = Kategori.objects.get(
                    kategori=existing_barang.kategori.kategori)
                lok = Lokasi.objects.get(
                    lokasi=existing_barang.lokasi.lokasi)

                # Simpan data ke BarangKeluar
                if not user:
                    barang_keluar_data = BarangKeluar.objects.create(
                        date_keluar=format_tanggal,
                        date_masuk=existing_barang.date,
                        device=device,
                        user=existing_barang.user,
                        lokasi=lok,
                        pc=existing_barang.pc,
                        os=existing_barang.os,
                        cpu=existing_barang.cpu,
                        vga=existing_barang.vga,
                        ram=existing_barang.ram,
                        model=existing_barang.model,
                        serialnumber=existing_barang.serialnumber,
                        description=existing_barang.description,
                        kategori=kat,
                        nama=penulis
                    )
                    title = "Barang Keluar"
                    content = f"Barang {barang_keluar_data.device} telah keluar pada tanggal {barang_keluar_data.date_keluar}."
                    Notification.objects.create(
                        title=title, content=content)
                    with transaction.atomic():
                        existing_barang.delete()
                    messages.success(
                        request, 'Data berhasil disimpan ke BarangKeluar dan dihapus dari BarangMasuk. ')
                    return redirect('barangkeluar')
                else:
                    barang_keluar_data = BarangKeluar.objects.create(
                        date_keluar=format_tanggal,
                        date_masuk=existing_barang.date,
                        device=device,
                        user=user,
                        lokasi=lok,
                        pc=existing_barang.pc,
                        os=existing_barang.os,
                        cpu=existing_barang.cpu,
                        vga=existing_barang.vga,
                        ram=existing_barang.ram,
                        model=existing_barang.model,
                        serialnumber=existing_barang.serialnumber,
                        description=existing_barang.description,
                        kategori=kat,
                        nama=penulis,
                    )
                    title = "Barang Keluar"
                    content = f"Barang {barang_keluar_data.device} telah keluar pada tanggal {barang_keluar_data.date_keluar}."
                    Notification.objects.create(
                        title=title, content=content)
                    with transaction.atomic():
                        existing_barang.delete()
                    messages.success(
                        request, 'Data berhasil disimpan ke BarangKeluar dan dihapus dari BarangMasuk.')
                    return redirect('barangkeluar')  # Ubah ke URL yang sesuai
        else:
            messages.error(request, 'Device belum terdaftar.')
    # form_data = {
    #     'device': '',
    #     'user': '',
    #     'email': '',
    #     'pc': '',
    #     'os': '',
    #     'cpu': '',
    #     'vga': '',
    #     'ram': '',
    #     'model': '',
    #     'serialnumber': '',
    #     'description': '',
    #     'kategori': '',
    # }
    form_data = {
        'device': request.POST.get('device', ''),
        'user': request.POST.get('user', ''),
        'lokasi': request.POST.get('lokasi', ''),
        'pc': request.POST.get('pc', ''),
        'os': request.POST.get('os', ''),
        'cpu': request.POST.get('cpu', ''),
        'vga': request.POST.get('vga', ''),
        'ram': request.POST.get('ram', ''),
        'model': request.POST.get('model', ''),
        'serialnumber': request.POST.get('serialnumber', ''),
        'description': request.POST.get('description', ''),
        'kategori': request.POST.get('kategori', ''),

    }
    form = {
        'form_data': form_data,
        'kategori': kategori,
    }
    context = {
        'kategori': kategori,
        'lokasi': lokasi,
        'barangmasuk': barangmasuk,
        'form': form,
    }
    return render(request, template_name, context,)


@login_required
def editBarangMasuk(request, id):
    template_name = "formbarangmasuk.html"
    get_item = BarangMasuk.objects.get(id=id)
    kategori = Kategori.objects.all()
    lokasi = Lokasi.objects.all()

    if request.method == 'POST':
        device = request.POST.get('device')
        user = request.POST.get('user')
        lokasi_name = request.POST.get('lokasi')
        lok = Lokasi.objects.get(lokasi=lokasi_name)
        pc = request.POST.get('pc')
        os = request.POST.get('os')
        cpu = request.POST.get('cpu')
        vga = request.POST.get('vga')
        ram = request.POST.get('ram')
        model = request.POST.get('model')
        serialnumber = request.POST.get('serialnumber')
        description = request.POST.get('description')
        # Change variable name to avoid conflict
        kategori_name = request.POST.get('kategori')
        kat = Kategori.objects.get(kategori=kategori_name)

        get_item.device = device
        get_item.user = user
        get_item.lokasi = lok
        get_item.pc = pc
        get_item.os = os
        get_item.cpu = cpu
        get_item.vga = vga
        get_item.ram = ram
        get_item.model = model
        get_item.serialnumber = serialnumber
        get_item.description = description
        get_item.kategori = kat
        get_item.save()

        return redirect(tbdatabarang)

    context = {
        "item_value": get_item,
        "kategori": kategori,
        "lokasi": lokasi,

    }
    return render(request, template_name, context)


@login_required
def deleteBarangMasuk(request, id):
    BarangMasuk.objects.get(id=id).delete()
    messages.success(request, 'Data berhasil dihapus.')
    return redirect(tbdatabarang)


@login_required
def deleteBarangKeluar(request, id):
    BarangKeluar.objects.get(id=id).delete()
    messages.success(request, 'Data berhasil dihapus.')
    return redirect(tbriwayatdata)


@login_required
def tbdatabarang(request):
    global results
    results = None
    template_name = "tbdatabarang.html"
    barang = BarangMasuk.objects.all()
    kategori = Kategori.objects.all()
    get_kategori = str(request.POST.get('kategori'))
    get_search = request.POST.get('search')
    print(get_search)
    search_category = BarangMasuk.objects.filter(
        kategori__kategori__contains=get_kategori)
    if get_search:

        queries = Q(date__icontains=get_search) | Q(device__icontains=get_search) | Q(user__icontains=get_search) | Q(email__icontains=get_search) | Q(pc__icontains=get_search) | Q(os__icontains=get_search) | Q(
            cpu__icontains=get_search) | Q(vga__icontains=get_search) | Q(ram__icontains=get_search) | Q(model__icontains=get_search) | Q(serialnumber__icontains=get_search) | Q(description__icontains=get_search)

        results = BarangMasuk.objects.filter(queries)

    elif get_kategori:
        results = BarangMasuk.objects.filter(
            kategori__kategori__contains=get_kategori)

    context = {
        'barang': barang,
        'kategori': kategori,
        's_kategori': search_category,
        'get_kategori': get_kategori,
        'get_search': get_search,
        'results': results,

    }

    return render(request, template_name, context)


@login_required
def tbriwayatdata(request):
    template_name = "tbriwayatbarang.html"
    global results
    results = None
    riwayatDT = BarangKeluar.objects.all()
    kategori = Kategori.objects.all()
    get_kategori = str(request.POST.get('kategori'))
    get_search = request.POST.get('search')
    print(get_kategori)
    print(get_search)
    search_category = BarangKeluar.objects.filter(
        kategori__kategori__contains=get_kategori)
    if get_search:

        queries = Q(date_masuk__icontains=get_search) | Q(date_keluar__icontains=get_search) | Q(device__icontains=get_search) | Q(user__icontains=get_search) | Q(email__icontains=get_search) | Q(pc__icontains=get_search) | Q(os__icontains=get_search) | Q(
            cpu__icontains=get_search) | Q(vga__icontains=get_search) | Q(ram__icontains=get_search) | Q(model__icontains=get_search) | Q(serialnumber__icontains=get_search) | Q(description__icontains=get_search)

        results = BarangKeluar.objects.filter(queries)

    elif get_kategori:
        results = BarangKeluar.objects.filter(
            kategori__kategori__contains=get_kategori)

    context = {
        "riwayatDT": riwayatDT,
        'kategori': kategori,
        's_kategori': search_category,
        'get_kategori': get_kategori,
        'get_search': get_search,
        'results': results,
    }
    return render(request, template_name, context)


def delete_selected(request):
    if request.method == "POST":
        selected_items_str = request.POST.get(
            "selected_items")  # Get the JSON string
        # Parse the JSON string to a Python list
        selected_items = json.loads(selected_items_str)

        try:
            for item_id in selected_items:
                item = BarangKeluar.objects.get(id=item_id)
                item.delete()

            messages.success(request, "Items deleted successfully.")
            return redirect(tbriwayatdata)
        except Exception as e:
            messages.error(request, "Error deleting items.")
            return redirect(tbriwayatdata)
    else:
        return redirect(tbriwayatdata)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "You have been logged in successfully")
            return redirect(analitic)
        else:
            messages.error(request, "Invalid username or password")
            return redirect(views.welcome)
    else:
        return render(request)


@login_required
@user_passes_test(is_operator)
def register(request):
    with transaction.atomic():
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email']
            get_password = request.POST['password']
            role = request.POST.get('role')  # Ambil peran dari formulir
            print(role)
            if User.objects.filter(username=email).exists():
                messages.error(request, "Username already exists")
                return redirect(tbuser)
            elif User.objects.filter(email=username).exists():
                messages.error(request, "Email already exists")
                return redirect(tbuser)
            else:
                user = User.objects.create(
                    username=email,
                    password=make_password(get_password),
                    first_name=first_name,
                    last_name=last_name,
                    email=username,)
                if role == 'superadmin':
                    user.is_staff = True
                    user.is_superuser = True
                else:
                    user.is_staff = False
                    user.is_superuser = False

                user.save()
                messages.success(request, "User created successfully")
                return redirect(tbuser)

        # Atur peran pengguna berdasarkan pilihan

        # Autentikasi pengguna dan masukkan ke dalam sesi
        user = authenticate(request, username=username, password=get_password)
        if user is not None:
            login(request, user)
            messages.success(request, "Registrasi berhasil.")
            # Ganti dengan URL halaman setelah pendaftaran
            return redirect('dashboard')
        else:
            messages.error(request, "Registrasi gagal. Silakan coba lagi.")

    return render(request, 'registration/register.html')


@login_required
@user_passes_test(is_operator)
def editUser(request, id):
    template_name = "tbuser.html"
    get_user = User.objects.get(id=id)
    user = User.objects.all()
    id_user = get_user.id
    print(get_user.id)

    print(id_user)
    with transaction.atomic():
        if request.method == 'POST':
            username = request.POST.get('username')
            get_password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            role = request.POST.get('role')
            if role == 'superadmin':
                get_user.is_staff = True
                get_user.is_superuser = True
            else:
                get_user.is_staff = False
                get_user.is_superuser = False
            get_user.username = email
            get_user.password = make_password(get_password)
            get_user.first_name = first_name
            get_user.last_name = last_name
            get_user.email = username
            get_user.save()

            return redirect(tbuser)

    context = {
        "users": get_user,
        "id_user": id_user,
        "test": "'',",
        'user': user,
    }

    return render(request, template_name, context)


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully")
    return redirect(views.welcome)


@login_required
@user_passes_test(is_operator)
def tbuser(request):
    template_name = "tbuser.html"
    user = User.objects.all()
    id_user = 0
    context = {
        'user': user,
        'id_user': id_user
    }
    return render(request, template_name, context)


@login_required
@user_passes_test(is_operator)
def hapusUsers(request, id):
    User.objects.get(id=id).delete()
    messages.success(request, "User has ben delete")
    return redirect(tbuser)


def export_to_csv(request):
    riwayattb = BarangKeluar.objects.all()
    response = HttpResponse('')
    response['Content-Disposition'] = 'attachment; filename=riwayat_data_export.csv'
    writer = csv.writer(response)
    writer.writerow(['Date Keluar', 'Date Masuk', 'Device', 'User', 'Email', 'Pc', 'Os', 'Cpu',
                    'Vga', 'Ram', 'Model', 'Serialnumber', 'Description', 'Kategori'])
    data_fields = riwayattb.values_list('date_keluar', 'date_masuk', 'device', 'user', 'email', 'pc', 'os', 'cpu',
                                        'vga', 'ram', 'model', 'serialnumber', 'description', 'kategori__kategori')
    for riwayattb in data_fields:
        writer.writerow(riwayattb)
    return response


@csrf_exempt
def fetch_notifications(request):
    unread_notifications = Notification.objects.filter(
        is_read=False).order_by("-timestamp")
    notifications = [
        {
            "id": notification.id,
            "title": notification.title,
            "content": notification.content
        }
        for notification in unread_notifications
    ]
    return JsonResponse({"notifications": notifications})


@csrf_exempt
def mark_notifications_as_read(request):
    if request.method == "POST":
        notification_ids = request.POST.getlist("notifications")
        Notification.objects.filter(
            id__in=notification_ids, is_read=True).delete()
        return JsonResponse({"message": "Notifications marked as read and deleted."})
    return JsonResponse({"error": "Invalid request method."}, status=400)


@csrf_exempt
def get_unread_notification_count(request):
    # Logic to get unread notification count from your database
    unread_count = Notification.objects.filter(is_read=False).count()

    return JsonResponse({"unread_count": unread_count})


@csrf_exempt
def delete_all_notifications(request):
    if request.method == "POST":
        Notification.objects.all().delete()
        return JsonResponse({"message": "All notifications deleted."})
    return JsonResponse({"error": "Invalid request method."}, status=400)


@login_required
@user_passes_test(is_operator)
def formkategory(request):
    template_name = "categoryForm.html"
    kategori = Kategori.objects.all()

    if request.method == 'POST':
        # Mengambil data dari input dengan name="kategori"
        kategori = request.POST.get('kategori')
        Kategori.objects.create(
            kategori=kategori)
        # Ganti dengan URL yang sesuai setelah berhasil input
        return redirect('kategory')
    context = {
        'kategori': kategori

    }
    return render(request, template_name, context)


@login_required
@user_passes_test(is_operator)
def formlokasi(request):
    template_name = "lokasiTable.html"
    lokasi = Lokasi.objects.all()

    if request.method == 'POST':
        # Mengambil data dari input dengan name="kategori"
        lokasi = request.POST.get('lokasi')
        Lokasi.objects.create(
            lokasi=lokasi)
        # Ganti dengan URL yang sesuai setelah berhasil input
        return redirect(formlokasi)
    context = {
        'lokasi': lokasi

    }
    return render(request, template_name, context)


@login_required
@user_passes_test(is_operator)
def deletekategori(request, id):
    Kategori.objects.get(id=id).delete()
    messages.success(request, 'Kategori berhasil dihapus')
    return redirect('kategory')


@login_required
@user_passes_test(is_operator)
def deletelokasi(request, id):
    Lokasi.objects.get(id=id).delete()
    messages.success(request, 'Lokasi berhasil dihapus')
    return redirect(formlokasi)
