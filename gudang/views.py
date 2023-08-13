from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import *
# Create your views here.


def dashboard(request):
    template_name = "base.html"

    return render(request, template_name)


def barangmasuk(request):
    template_name = "formbarangmasuk.html"
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
        kategori = request.POST.get('kategori')
        kat = Kategori.objects.get(kategori=kategori)
        BarangMasuk.objects.create(
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

    context = {
        'kategori': kategori,
    }
    return render(request, template_name, context)


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


def tbdatabarang(request):
    template_name = "tbdatabarang.html"
    barang = BarangMasuk.objects.all()
    context = {
        'barang': barang,
    }
    return render(request, template_name, context)
