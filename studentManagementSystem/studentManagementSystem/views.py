from django.shortcuts import render, redirect, HttpResponse
from CampusEase.EmailBackEnd import EmailBackEnd
from CampusEase.models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


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

@login_required(login_url='/')
def PROFILE(request):
    user = CustomUser.objects.get(id = request.user.id)
    context = {
        'user': user,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='/')
def PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        # username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        # email = request.POST.get('email')

        try:
            customuser = CustomUser.objects.get(id = request.user.id)

            customuser.first_name = first_name
            customuser.last_name = last_name

            if profile_pic != None and profile_pic != "":
                customuser.profile_pic = profile_pic

            customuser.save()
            messages.success(request, 'Profile Updated Successfully')

            redirect('profile')

        except:
            messages.error(request, 'Failed to Update Profile')

    return render(request, 'profile.html')

@login_required(login_url='/')
def PASSWORD_UPDATE(request):
    if request.method == "POST":
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        try:
            user = request.user

            # Check if the old password matches the current password
            if not user.check_password(old_password):
                raise ValueError('Old password is incorrect.')

            # Check if new passwords match
            if new_password1 != new_password2:
                raise ValueError('New passwords do not match.')

            # Change the user's password
            user.set_password(new_password1)
            user.save()

            # Update the session with the new password
            update_session_auth_hash(request, user)

            messages.success(request, 'Password updated successfully.')
            return redirect('profile')

        except ValueError as e:
            messages.error(request, str(e))
            return render(request, 'password_change.html')

        except Exception as e:
            messages.error(request, 'Failed to update password.')
            return render(request, 'password_change.html')

    return render(request, 'profile.html')

