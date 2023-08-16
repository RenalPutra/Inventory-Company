from .models import Kategori, BarangKeluar
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.db.models import Q
from django.db import transaction
from django.http import HttpResponseRedirect
from .models import *
from datetime import datetime 
# Create your views here.


def analitic(request):
    template_name = "analitic.html"

    # Menghitung total data masuk dan data keluar
    total_data_masuk = BarangMasuk.objects.count()
    total_data_keluar = BarangKeluar.objects.count()

    # Mengambil 5 recent activity data masuk dan data keluar terbaru
    recent_activity_masuk = BarangMasuk.objects.order_by('-date')[:5]
    recent_activity_keluar = BarangKeluar.objects.order_by('-date')[:5]

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
            'joined': activity.date,
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


def dashboard(request):
    template_name = "base.html"

    return render(request, template_name)


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
                    'date_keluar':format_tanggal,
                    'date_masuk':existing_barang.date,
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


def deleteBarangMasuk(request, id):
    BarangMasuk.objects.get(id=id).delete()
    return redirect(tbdatabarang)

def deleteBarangKeluar(request, id):
    BarangKeluar.objects.get(id=id).delete()
    return redirect(tbriwayatdata)


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
        "riwayatDT" : riwayatDT,
        'kategori': kategori,
        's_kategori': search_category,
        'get_kategori': get_kategori,
        'get_search': get_search,
        'results': results,
    }
    return render(request, template_name, context)