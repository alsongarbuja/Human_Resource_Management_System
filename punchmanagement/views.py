from django.shortcuts import render


def clockInOut(request):

  return render(request, "punch/clock-in-out.html")
