from django.shortcuts import render

def login(request):
  return render(request, "auth/login.html")

def dashboard(request):
  return render(request, "app/dashboard.html")
