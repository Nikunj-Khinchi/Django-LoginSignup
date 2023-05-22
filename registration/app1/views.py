from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.


@login_required(login_url='login')
def HomePage(request):
    user = request.user  # Get the current authenticated user
    context = {
        'username': user.username.upper(),
        'email': user.email,
    }
    return render(request, 'home.html', context)
   


def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')


        if not uname or not email or not pass1 or not pass2:
            messages.error(request, '*All fields are required.')
            return redirect('signup')
        

        if pass1 != pass2:
            messages.error(request, "*Passwords must be same")
            return redirect("signup")
          
        else:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            
            print(uname, " ", email, " ", pass1, " ", pass2)
            
            messages.success(request, 'User has been created successfully.', extra_tags='success')


    return render(request, 'signup.html')


def LoginPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=uname, password=pass1)

        if not uname or not pass1:
            messages.error(request, 'Please fill in all fields.')
            return redirect('login')
            
        else:

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid details')
                return redirect('login')

        

    return render(request, 'login.html')


def LogoutPage(request):
    logout(request)
    return redirect('login')
