from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.
def home(request):
    return render(request,'home.html')

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username').lower()
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
 
        if User.objects.filter(username = username):
            messages.error(request,"Username already exists,please try another username")
            return redirect('signup')
        
        if User.objects.filter(email = email):
            messages.error(request,"email already used,please try another email")
            return redirect('signup')
        
        if pass1 != pass2:
            messages.error(request,"password do not match")
            return redirect('signup')

        if len(pass1)< 8:
            messages.error(request,"password must be atleast 8 charaters") 

        user = User.objects.create_user(username,email,pass1)
        user.first_name=fname
        user.last_name=lname
        user.save()

         #Welcome Email
        subject = "Welcome to saviour developers"
        message = f"Hello" + user.first_name + " \n"+"Welcome to our backend developers company"
        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email]
        send_mail( subject,message,from_email,to_list)

        messages.success(request,'Your account has been created successfully, weve send you a confirmation email')
        
        return redirect('login')
        
    return render(request,'authentication/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')

        user1 = authenticate(username = username ,password = pass1)

        if user1 is not None:
            login(request, user1)
            fname = user1.first_name
            messages.success(request,"you've logged in succesfully")
            return render(request,"index.html",{'fname':fname})
        
        else:
            messages.error(request,"bad credentials")
            return redirect('login')
        
    return render(request,'authentication/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

    #password = yydcsofhrmvtlqvd