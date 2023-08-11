from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

def dashboard(request):
    template_name = "dashboard.html"
    
    return render(request, template_name)