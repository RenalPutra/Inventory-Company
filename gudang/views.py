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
            'device': activity.device,  # 'device' adalah nama field di model 'BarangMasuk
            'name': activity.user,
            'email': activity.email,
            'joined': activity.date,
            'type': 'Data Masuk',
            'status': 'Liked'  # Anda dapat mengganti ini sesuai dengan kebutuhan
        })
    for activity in recent_activity_keluar:
        recent_activity.append({
            'device': activity.device,  # 'device' adalah nama field di model 'BarangKeluar
            'name': activity.user,
            'email': activity.email,
            'joined': activity.date_keluar,
            'type': 'Data Keluar',
            'status': 'Liked'  # Anda dapat mengganti ini sesuai dengan kebutuhan
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
    waktu_sekarang = datetime.now()
    format_tanggal = waktu_sekarang.strftime("%a %m %Y - %H:%M:%S")
    if request.method == 'POST':
        device = request.POST.get('device')
        user = request.POST.get('user')
        email = request.POST.get('email')
        pc = request.POST.get('pc')
        os = request.POST.get('os')
        cpu = request.POST.get('cpu')
        vga = request.POST.get('vga')
        ram = request.POST.get('ram')
        model = request.POST.get('model')
        serialnumber = request.POST.get('serialnumber')
        description = request.POST.get('description')
        kategori = request.POST.get('kategori')
        # jika data kategori tidak ada maka akan muncul pesan error

        if not kategori:
            messages.error(
                request, 'Kategori tidak boleh kosong')
            return redirect('barangmasuk')
        else:
            kat = Kategori.objects.get(kategori=kategori)
            BarangMasuk.objects.create(
                date=format_tanggal,
                device=device,
                user=user,
                email=email,
                pc=pc,
                os=os,
                cpu=cpu,
                vga=vga,
                ram=ram,
                model=model,
                serialnumber=serialnumber,
                description=description,
                kategori=kat
            )
            messages.success(
                request, 'Data berhasil disimpan')

    context = {
        'kategori': kategori,
    }

    return render(request, template_name, context)

# jika barang keluar user hanya perlu mengisi Device saja
# dan data lainnya akan otomatis terisi
# jika device tidak ada maka akan muncul pesan error


@login_required
def barangkeluar(request):
    template_name = "formbarangkeluar.html"
    kategori = Kategori.objects.all()
    kategori = Kategori.objects.all()
    waktu_sekarang = datetime.now()
    format_tanggal = waktu_sekarang.strftime("%a %m %Y - %H:%M:%S")

    if request.method == 'POST':
        device = request.POST.get('device')
        existing_barang = BarangMasuk.objects.filter(device=device).first()

        if existing_barang:
            if 'submit_form' in request.POST:
                # Jika tombol "Submit" ditekan, simpan data ke BarangKeluar
                form_data = {
                    'date_keluar': format_tanggal,
                    'date_masuk': existing_barang.date,
                    'device': existing_barang.device,
                    'user': existing_barang.user,
                    'email': existing_barang.email,
                    'pc': existing_barang.pc,
                    'os': existing_barang.os,
                    'cpu': existing_barang.cpu,
                    'vga': existing_barang.vga,
                    'ram': existing_barang.ram,
                    'model': existing_barang.model,
                    'serialnumber': existing_barang.serialnumber,
                    'description': existing_barang.description,
                    'kategori': existing_barang.kategori.kategori,
                }
                kat = Kategori.objects.get(
                    kategori=existing_barang.kategori.kategori)
                # Simpan data ke BarangKeluar
                BarangKeluar.objects.create(
                    date_keluar=format_tanggal,
                    date_masuk=existing_barang.date,
                    device=device,
                    user=existing_barang.user,
                    email=existing_barang.email,
                    pc=existing_barang.pc,
                    os=existing_barang.os,
                    cpu=existing_barang.cpu,
                    vga=existing_barang.vga,
                    ram=existing_barang.ram,
                    model=existing_barang.model,
                    serialnumber=existing_barang.serialnumber,
                    description=existing_barang.description,
                    kategori=kat
                )
                with transaction.atomic():
                    existing_barang.delete()

                messages.success(
                    request, 'Data berhasil disimpan ke BarangKeluar dan dihapus dari BarangMasuk.')
                return redirect('barangkeluar')  # Ubah ke URL yang sesuai

        else:
            messages.error(request, 'Device belum terdaftar.')

    form_data = {
        'device': '',
        'user': '',
        'email': '',
        'pc': '',
        'os': '',
        'cpu': '',
        'vga': '',
        'ram': '',
        'model': '',
        'serialnumber': '',
        'description': '',
        'kategori': '',
    }

    form = {
        'form_data': form_data,
        'kategori': kategori,
    }

    context = {
        'kategori': kategori,
    }
    return render(request, template_name, context,)


@login_required
def editBarangMasuk(request, id):
    template_name = "formbarangmasuk.html"
    get_item = BarangMasuk.objects.get(id=id)
    kategori = Kategori.objects.all()

    if request.method == 'POST':
        device = request.POST.get('device')
        user = request.POST.get('user')
        email = request.POST.get('email')
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
        get_item.email = email
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
    }

    return render(request, template_name, context)


@login_required
def deleteBarangMasuk(request, id):
    BarangMasuk.objects.get(id=id).delete()
    return redirect(tbdatabarang)


@login_required
def deleteBarangKeluar(request, id):
    BarangKeluar.objects.get(id=id).delete()
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
    search_category = BarangMasuk.objects.filter(
        kategori__kategori__contains=get_kategori)
    if get_search:

        queries = Q(device__icontains=get_search) | Q(user__icontains=get_search) | Q(email__icontains=get_search) | Q(pc__icontains=get_search) | Q(os__icontains=get_search) | Q(
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
    search_category = BarangKeluar.objects.filter(
        kategori__kategori__contains=get_kategori)
    if get_search:

        queries = Q(device__icontains=get_search) | Q(user__icontains=get_search) | Q(email__icontains=get_search) | Q(pc__icontains=get_search) | Q(os__icontains=get_search) | Q(
            cpu__icontains=get_search) | Q(vga__icontains=get_search) | Q(ram__icontains=get_search) | Q(model__icontains=get_search) | Q(serialnumber__icontains=get_search) | Q(description__icontains=get_search)

        results = barangsearch_category = BarangKeluar.objects.filter(queries)

    elif get_kategori:
        results = barangsearch_category = BarangKeluar.objects.filter(
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
            username = request.POST.get('username')
            get_password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return redirect(tbuser)
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
                return redirect(tbuser)
            else:
                User.objects.create(
                username = username,
                password = make_password(get_password),
                first_name = first_name,
                last_name = last_name,
                email = email,)
                messages.success(request, "User created successfully")
                return redirect(tbuser)
        else:
            form = UserCreationForm()
            
    context = {
        'title': 'Register',
        'form': form,
    }
    
    return render(request, context)

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
            print(first_name)
            print(last_name)

            get_user.username = username
            get_user.password = make_password(get_password)
            get_user.first_name = first_name
            get_user.last_name = last_name
            get_user.email = email
            get_user.save()
        
            return redirect(tbuser)
    
    
        
    context = {
        "users" : get_user,
        "id_user" : id_user,
        "test" : "'',",
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
        'id_user' : id_user
    }
    return render(request, template_name, context)

@login_required
@user_passes_test(is_operator)
def hapusUsers(request, id):
    User.objects.get(id=id).delete()
    return redirect(tbuser)

def export_to_csv(request):
    riwayattb = BarangKeluar.objects.all()
    response = HttpResponse('')
    response['Content-Disposition'] = 'attachment; filename=riwayat_data_export.csv'
    writer = csv.writer(response)
    writer.writerow(['Date Keluar', 'Date Masuk', 'Device', 'User', 'Email', 'Pc', 'Os', 'Cpu',
                    'Vga', 'Ram', 'Model', 'Serialnumber', 'Description', 'Kategori'])
    data_fields = riwayattb.values_list('date_keluar', 'date_masuk', 'device', 'user', 'email', 'pc', 'os', 'cpu',
                    'vga', 'ram', 'model', 'serialnumber', 'description', 'kategori')
    for riwayattb in data_fields:
        writer.writerow(riwayattb)
    return response
    