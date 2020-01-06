from django.shortcuts import render
from  .models import *
from django.http import HttpResponse
# Create your views here.
def GetCommune(request,id=0):
    if id!=0:
        # try:
        communes=Commune.objects.filter(wilaya__id=id)
        return render(request,'region/commune_select.html',{'communes':communes})
    #     except:
    #         return HttpResponse(status=500)
    # else:
    #     return HttpResponse(status=401)
