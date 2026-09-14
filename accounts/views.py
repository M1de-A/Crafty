from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render,redirect
from .forms import RegisterForm,ProfileForm

def register(request):
    if request.user.is_authenticated:return redirect('account')
    form=RegisterForm(request.POST or None)
    if form.is_valid(): login(request,form.save()); return redirect('account')
    return render(request,'registration/register.html',{'form':form})

def site_login(request):
    if request.user.is_authenticated:
        return redirect('/admin/' if request.user.is_superuser else 'account')
    form=AuthenticationForm(request,data=request.POST or None)
    if request.method=='POST' and form.is_valid():
        user=form.get_user(); login(request,user)
        return redirect('/admin/' if user.is_superuser else 'account')
    return render(request,'registration/login.html',{'form':form})

@login_required
def account(request):
    if request.user.is_superuser: return redirect('/admin/')
    profile=request.user.profile
    if request.method=='POST':
        form=ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid(): form.save(); return redirect('account')
    else: form=ProfileForm(instance=profile)
    return render(request,'accounts/account.html',{'profile':profile,'profile_form':form})
