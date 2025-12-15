from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'MainApps/home.html')


def service_pricing(request):
    return render(request,'MainApps/service_pricing.html')