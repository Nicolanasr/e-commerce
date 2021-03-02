from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import CreateUserForm, ChangeUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required



# Create your views here.


def index(request):
    return redirect('store:index')


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('index:index')
    else:
        form = CreateUserForm()
        ctx = {'form': form}
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                username = request.POST.get('username')
                password = request.POST.get('password1')
                form.save()
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                return redirect('index:index')
            else:
                err = form.errors.values()
            err = list(err)
            ctx = {'form': form, 'err': err}
            print(err)
            return render(request, 'index/register.html', ctx)

        return render(request, 'index/register.html', ctx)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index:index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                return redirect('index:index')
            else:
                messages.warning(request, 'Username or Password are incorrect')
        return render(request, 'index/login.html')


@login_required(login_url='index:login')
def logoutPage(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('index:index')
    else:
        return redirect('index:login')

@login_required(login_url='index:login')
def userAccount(request, user):
    if request.user.username == user:
        user = get_object_or_404(User, username=user)
        if request.method == 'POST':
            form = ChangeUserForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
            
            err = form.errors.values()
            err = list(err)
            ctx = {'form': form, 'err': err}
            return render(request, 'index/account.html', ctx)


        form = ChangeUserForm(instance=user)
        ctx = {'form': form}
        return render(request, 'index/account.html', ctx)
    else:
        print(user, request.user)
        return redirect('index:index')

@login_required(login_url='index:login')
def forgotPassword(request, user):
    form = PasswordChangeForm(user)
    ctx = {'form': form}
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('index:userAccount', request.user)
        else:
            err = form.errors.values()
            err = list(err)
            ctx = {'form': form, 'err': err}
        
    return render(request, 'index/passwordforgot.html', ctx)