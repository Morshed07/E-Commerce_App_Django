from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.urls import reverse

# Create your views here.
def home(request):
    return render(request, 'index.html')

def AdminLogin(request):
    return render(request, 'admin_templates/signin.html')

def AdminloginProcess(request):
    username=request.POST['username']
    password=request.POST['password']

    user=authenticate(request=request,username=username,password=password)
    if user is not None:
        login(request=request, user=user)
        return HttpResponseRedirect(reverse("admin_home"))
    else:
        messages.error(request, "Invalid Login Details!")
        return HttpResponseRedirect(reverse("admin_login"))

def AdminlogoutProcess(request):
    logout(request)
    messages.success(request, "Logout Succesfully!")
    return HttpResponseRedirect(reverse("admin_login"))