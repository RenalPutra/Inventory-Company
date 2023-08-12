from django.shortcuts import render
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


def tbdatabarang(request):
    template_name = "tbdatabarang.html"
    barang = BarangMasuk.objects.all()
    context = {
        'barang': barang,
    }
    return render(request, template_name, context)
