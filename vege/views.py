from django.contrib import messages
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from .models import *
# Create your views here.

def Getting_information():
    query = Receipe.objects.all()
    context = {'receipes': query}
    return context


@login_required(login_url='/login/')
def base(request):
    context={}
    return render(request,'receipe.html',context)

def index(request):
    if request.method=='POST':
        data = request.POST
        receipe_name=data.get('receipe_name')
        receipe_description=data.get('receipe_description')
        receipe_image = request.FILES.get('receipe_image')
        print(receipe_name)
        Receipe.objects.create(
            receipe_name=receipe_name,
            receipe_description=receipe_description,
            receipe_image=receipe_image
        )
        return redirect('recipe/')

    context = Getting_information()
    if request.GET.get('receipe_name'):
        querryset= context['receipes']
        query=querryset.filter(receipe_name__icontains = request.GET.get('receipe_name'))
        context = {'receipes': query}
    return render(request,'receipe.html',context)

def delete(request,id):
    obj =Receipe.objects.get(receipe_name=id)
    obj.delete()
    context = Getting_information()
    return render(request, 'receipe.html', context)

def update(request,id):
    query =Receipe.objects.get(receipe_name=id)

    if request.method  == 'POST':
        data = request.POST
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        receipe_image = request.FILES.get('receipe_image')

        query.receipe_name=receipe_name
        query.receipe_description=receipe_description

        if receipe_image:
            query.receipe_image = receipe_image

        query.save()
        return redirect('recipe/')

    context = {'receipes':query}
    return render(request,'update.html',context)


def register(request):
    if request.method == 'POST':
        from django.contrib.auth.models import User
        data = request.POST
        first_name=data.get('first')
        last_name = data.get('last')
        username=data.get('username')
        email = data.get('email')
        password = data.get('password_user')

        if User.objects.filter(username=username).exists():
            messages.error(request,'Username already exits please change Username')
            return redirect('/register')

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email= email
        )

        # Set password and save user
        user.set_password(password)
        user.save()
        return redirect('/login/')
    return render(request,'register.html')
def login_page(request):

    if request.method == 'POST':
        data = request.POST

        username = data.get('username')
        password = data.get('password')
        if not (User.objects.filter(username=username).exists()):
            messages.error(request,'Invalid Username')
            return redirect('/login/')

        user=authenticate(request,username=username,password=password)

        if user is None:
            messages.error(request,'Invalid password')
            return redirect('/login/')
        else:
            login(request,user)
            messages.info(request,'Login sucessfully')
            return redirect('/recipe/')
    return render(request,'login.html')

def logout_page(request):
    messages.info(request,'logout')
    logout(request)
    return redirect('/login/')



