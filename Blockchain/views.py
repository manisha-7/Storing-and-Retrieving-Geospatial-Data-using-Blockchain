from datetime import datetime, date
from threading import Thread
import time
import rasterio

from django.shortcuts import render, HttpResponse, redirect
from .forms import MyfileUploadForm
from .models import file_upload
from Blockchain import ipfs_ext, smartcontract
import os
from Blockchain import password_generate as pg
import re
import rasterio
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, auth, Group
from django.conf import settings
from .decorators import allowed_users, unauthenticated_user
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from django.core.mail import send_mail
from Blockchain.pdf_pass import convtpdf
datelast = date.today()

@login_required(login_url='login')
def upload(request):

    form= MyfileUploadForm()

    if request.method == 'POST':
        
        form = MyfileUploadForm(request.POST,request.FILES)

        if form.is_valid():
            userkanaam = User.objects.get(username=str(request.user.username))
            # Coordinate = str(request.POST['coordinate']).lower()
            date = request.POST['date']
            Location = str(request.POST['location']).lower()
            Satellite = str(request.POST['satellite']).lower()
            type_of_data = request.POST['type_of_data']
            viewusers = list(map(str,(str(request.POST['viewusers']).split(','))))
            the_files = form.cleaned_data['files_data']
            Coordinate = rasterio.open(the_files)
            Coordinate = f'{Coordinate.bounds[0], Coordinate.bounds[1], Coordinate.bounds[2], Coordinate.bounds[3]}'
            print(Coordinate)
            fil = file_upload(Coordinate=Coordinate, date=date, Location=Location, Satellite=Satellite, type_of_data=type_of_data, my_file=the_files)
            fil.save()
            ipfshash = ipfs_ext.func()
            smartcontract.add_block(Coordinate=Coordinate, date=date, Location=Location, Satellite=Satellite, type_of_data=type_of_data, ipfshash=ipfshash, viewusers=viewusers, userkanaam=(userkanaam))
            fil.delete()
            return render(request, 'upload.html',)
        else:
            return HttpResponse('error')

    else:
        
        context = {
            'form':MyfileUploadForm
        }      
        
        return render(request, 'upload.html', context)
    
    
@login_required(login_url='login')
def home(request):
    user = User.objects.get(username=str(request.user.username))
    group = Group(name='super_user')
    context = {}
    if user.groups.filter(name=group):
        context = {'groupss' : 'super_user'}
        
    group = Group(name='admin')
    if user.groups.filter(name=group):
        context = {'groupss' : 'admin'}
        
    group = Group(name='employee')
    if user.groups.filter(name=group):
        context = {'groupss' : 'employee'}
    
    
    return render(request,'home.html', context)
    

@login_required(login_url='login')
@allowed_users(allowed_roles=['super_user'])
def register(request):
    context={}
    if request.method == 'POST':
        first_name = str(request.POST['first_name']).lower()
        last_name = str(request.POST['last_name']).lower()
        username = str(request.POST['username']).lower()
        email = str(request.POST['email']).lower()
        type_of_member = request.POST['type_of_member']
        password = pg.generate()
        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        user.save()
        userid = User.objects.get(username=str(username))
        send_mail(username, password, email)
        if type_of_member == 'super_user':
            g = Group.objects.get(name='super_user')
            g.user_set.add(userid.id)
        elif type_of_member == 'admin':
            g = Group.objects.get(name='admin')
            g.user_set.add(userid.id)
        elif type_of_member == 'employee':
            g = Group.objects.get(name='employee')
            g.user_set.add(userid.id)
            
        
    return render(request,'register.html',context)
  
  

def userlogin(request):
    if request.method == 'POST':
        username=str(request.POST.get('username')).lower()
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username or pass incorect')
                
    return render(request,'login.html')
    

   

def logoutUser(request):
   logout(request)
   return redirect('login')


@login_required(login_url='login')
def view(request):
   return render(request,'view.html')  
    
@login_required(login_url='login')
def search(request):
    if request.method == 'POST':
        timetaken = datetime.now()
        k = []
        coordinate=str(request.POST.get('coordinate')).lower()
        startdate = request.POST.get('startdate')
        enddate = request.POST.get('enddate')
        location = str(request.POST.get('location')).lower()
        datatype = request.POST.get('type_of_data')
        satellite = str(request.POST.get('satellite')).lower()
        k = smartcontract.extractdata(coordinate, startdate, enddate, location, datatype, satellite)
        context = {
            'datass' : k
        }
        user = User.objects.get(username=str(request.user.username))
        group = Group(name='super_user')
        context = {}
        if user.groups.filter(name=group):
            context = {
                'groupss' : 'super_user',
                'datass' : k,
                'user' : str(user)
            }
            
        group = Group(name='admin')
        if user.groups.filter(name=group):
            context = {
                'groupss' : 'admin',
                'datass' : k,
                'user' : str(user)
                }
            
        group = Group(name='employee')
        if user.groups.filter(name=group):
            context = {
                'groupss' : 'employee',
                'datass' : k,
                'user' : str(user)
                }
        return render(request,'view.html', context)    
    return render(request,'search.html')    


@login_required(login_url='login')
def resetpass(request):
    users = User.objects.all()
    for u in users:
        if str(u) != 'admin':   
            g = User.objects.get(username__exact=str(u))
            user_email = (g.email)
            email=request.POST.get("email")
            passwd = pg.generate()
            g.set_password(passwd)
            g.save()
            send_mail(u, passwd, user_email)
            
    return redirect('login')

@login_required(login_url='login')
def resetpassd(request):
    users = User.objects.all()
    for u in users:
        if str(u) != 'admin':   
            g = User.objects.get(username__exact=str(u))
            user_email = (g.email)
            email=request.POST.get("email")
            passwd = pg.generate()
            g.set_password(passwd)
            g.save()
            send_mail(u, passwd, user_email)
            
    datelast = date.today()

def res(request):
    global datelast
    while True:
        if str(datelast - date.today()) == '30 days':
            users = User.objects.all()
            for u in users:
                if str(u) != 'admin':   
                    g = User.objects.get(username__exact=str(u))
                    user_email = (g.email)
                    passwd = pg.generate()
                    g.set_password(passwd)
                    g.save()
                    send_mail(u, passwd, user_email)
            datelast = date.today()
        time.sleep(2628000)

  


# t1 = Thread(target=res)
# t1.start()

def send_mail(username, password, email):
    mydict = {'username': username, 'password': password, 'email': email}
    convtpdf(username, password)
    html_template = 'register_email.html'
    html_message = render_to_string(html_template, context=mydict)
    subject = 'Welcome to Service-Verse'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    message = EmailMessage(subject, html_message,
                            email_from, recipient_list)
    message.content_subtype = 'html'
    
    message.attach_file('password1.pdf')
    message.send()
    os.remove('password.pdf')
    os.remove('password1.pdf')
    
def downloads(request):
    if request.method == 'POST':
        download = request.POST.get('download')
        (os.system(f"ipfs get {download}"))
        print(download)
    return render(request,'search.html')  


def homepage(request):
    return render(request,'homepage.html')  

def about(request):
    return render(request,'about.html')  

@login_required(login_url='login')
def modify_permissions(request):
    if request.method == 'POST':
        val=str(request.POST.get('modify_permission'))
        k = smartcontract.modify_per(val)
        l = ','
        context = {
            'user' : l.join([str(i) for i in k['datas']['viewusers']]),
            'users' : k['datas']['viewusers'],
            'val' : val
        }
        return render(request, 'permissions.html', context)
    return render(request, 'permissions.html')

@login_required(login_url='login')
def ppermission(request):
    if request.method == 'POST':
        addp = request.POST.get('add_permission')
        rp = request.POST.get('remove_permission')
        val = request.POST.get('vall')
        smartcontract.makechange(val, addp, rp)
        return HttpResponse('ok')
    return HttpResponse('ok')
        