from django.shortcuts import render
from django.contrib.auth.decorators import permission_required

# @permission_required("")
def clockInOut(request):

  return render(request, "punch/clock-in-out.html")
