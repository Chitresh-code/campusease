from django.shortcuts import render, redirect, HttpResponse
from CampusEase.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def BASE(request):
    return render(request, 'base.html')

def LOGIN(request):
    return render(request, 'login.html')

def doLogin(request):
    if request.method == "POST":
        user = EmailBackEnd.authenticate(request,
                                         username=request.POST.get('email'),
                                         password=request.POST.get('password'),)
        if user != None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('hod_home')
            elif user_type == '2':
                return HttpResponse('This is Staff Panel')
            elif user_type == '3':
                return HttpResponse('This is Student Panel')
            else:
                messages.error(request, 'Invalid Email or Password')
                return redirect('login')
        else:
            messages.error(request, 'Invalid Email or Password')
            return redirect('login')


def doLogout(request):
    logout(request)
    return redirect('login')