from django.shortcuts import render, redirect
from django.db.models import Q
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
    
    global results
    results = None
    template_name = "tbdatabarang.html"
    barang = BarangMasuk.objects.all()
    kategori = Kategori.objects.all()
    get_kategori = str(request.POST.get('kategori'))
    get_search = request.POST.get('search')
    search_category = BarangMasuk.objects.filter(kategori__kategori__contains=get_kategori)
    if get_search:

        queries = Q(device__icontains=get_search) | Q(user__icontains=get_search) | Q(email__icontains=get_search) | Q(pc__icontains=get_search) | Q(os__icontains=get_search) |  Q(cpu__icontains=get_search) | Q(vga__icontains=get_search) | Q(ram__icontains=get_search) | Q(model__icontains=get_search) | Q(serialnumber__icontains=get_search) | Q(description__icontains=get_search)
        
        results = BarangMasuk.objects.filter(queries)
        
    elif get_kategori:
        results = BarangMasuk.objects.filter(kategori__kategori__contains=get_kategori)

        
    
    
    context = {
        'barang': barang,
        'kategori': kategori,
        's_kategori' : search_category,
        'get_kategori' : get_kategori,
        'get_search' :get_search,
        'results': results, 
    
    }
   
    
  
    


    return render(request, template_name, context)
