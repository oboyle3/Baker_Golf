from django.shortcuts import render, redirect
from .models import User, Golfer
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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


# @login_required
# def update_favorite_golfers(request):
#     user = request.user
#     all_golfers = Golfer.objects.all()  # Fetch all golfers

#     if request.method == "POST":
#         selected_golfers = request.POST.getlist('golfers')  # Get selected golfer IDs
        
#         if len(selected_golfers) > 5:  # Restrict to 5 golfers
#             messages.error(request, "You can only select up to 5 golfers.")
#         else:
#             user.favorite_golfers.set(selected_golfers)  # Update user's favorite golfers
#             messages.success(request, "Favorite golfers updated successfully!")
#             return redirect('update_favorites')

#     return render(request, 'update_favorites.html', {'all_golfers': all_golfers, 'user': user})
@login_required
def update_favorite_golfers(request):
    user = request.user
    golfers_by_tier = {}

    # Group golfers by tier
    for golfer in Golfer.objects.all():
        if golfer.tier not in golfers_by_tier:
            golfers_by_tier[golfer.tier] = []
        golfers_by_tier[golfer.tier].append(golfer)

    if request.method == "POST":
        selected_golfers = []
        
        # Extract one selected golfer per tier
        for tier in golfers_by_tier.keys():
            golfer_id = request.POST.get(f"tier_{tier}")
            if golfer_id:
                selected_golfers.append(golfer_id)

        if len(selected_golfers) != 3:  # Ensure exactly 3 golfers are selected
            messages.error(request, "You must select exactly one golfer per tier.")
        else:
            user.favorite_golfers.set(selected_golfers)  # Update user's favorite golfers
            messages.success(request, "Favorite golfers updated successfully!")
            return redirect('update_favorites')

    return render(request, 'update_favorites.html', {'golfers_by_tier': golfers_by_tier, 'user': user})


@login_required
def updatepage(request):
    return render(request, 'updatepage.html')  # Make sure 'blank.html' exists
