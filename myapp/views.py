from django.shortcuts import render, redirect
from .models import User, Golfer
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        print(request.POST)  # This will print the POST data to the console
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)  # This is how authentication is done
        if user is not None:
            login(request, user)
            return redirect('cars')  # Redirect to cars or user dashboard
        else:
            return render(request, 'login.html', {'error': 'Invalid email or password'})

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect back to the login page


@login_required
def cars_view(request):
    #golfers = Golfer.objects.all()  # taking this out 4_1
    #golfers = request.user.golfers.all()  # Many-to-many relationship from user to golfers
    golfers = request.user.favorite_golfers.all()  # Corrected ManyToMany access

    context = {
        'user': request.user,  # Pass the logged-in user
        'golfers': golfers  # Pass golfers to template
    }

    print("Golfers sent to template:", golfers)  # Debugging

    return render(request, 'cars.html', context)
