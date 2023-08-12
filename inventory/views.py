from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect


# def dashboard(request):
#     template_name = "base.html"

#     return render(request, template_name)


def welcome(request):
    template_name = "welcome.html"
    return render(request, template_name)


# def barangmasuk(request):
#     template_name = "formbarangmasuk.html"
#     return render(request, template_name)


# def tbdatabarang(request):
#     template_name = "tbdatabarang.html"
#     return render(request, template_name)
