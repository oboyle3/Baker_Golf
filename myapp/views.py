from django.shortcuts import render, redirect
from .models import User, Golfer , AllUsersFavoriteGolfers
from django.contrib.auth import authenticate, login, logout
#from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import FavoriteGolfersForm, SignUpForm


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
#     golfers_by_tier = {}

#     # Group golfers by tier
#     for golfer in Golfer.objects.all():
#         golfers_by_tier.setdefault(golfer.tier, []).append(golfer)

#     if request.method == "POST":
#         selected_golfers = []

#         # Collect the selected golfer IDs
#         for tier in golfers_by_tier.keys():
#             golfer_id = request.POST.get(f"tier_{tier}")
#             if golfer_id:
#                 selected_golfers.append(int(golfer_id))

#         print("Selected golfer IDs:", selected_golfers)
#         print("User ID:", user.id)

#         if len(selected_golfers) != 3:
#             messages.error(request, "You must select exactly one golfer per tier.")
#         else:
#             # Before creating, let's clear existing favorite golfers from the intermediary table
#             print("Clearing existing favorite golfers for user:", user.id)
#             AllUsersFavoriteGolfers.objects.filter(user=user).delete()
#             print("Old favorites cleared.")

#             # Add the new selected golfers to the intermediary table
#             for golfer_id in selected_golfers:
#                 print(f"Creating new favorite for golfer_id: {golfer_id} and user_id: {user.id}")
#                 AllUsersFavoriteGolfers.objects.create(user=user, golfer_id=golfer_id)
            
#             print("New favorites added.")

#             messages.success(request, "Favorite golfers updated successfully!")
#             return redirect("update_favorites")

#     return render(request, "update_favorites.html", {"golfers_by_tier": golfers_by_tier, "user": user})
@login_required  # Ensure the user is logged in
def update_favorite_golfers(request):
    # Get the current user
    user = request.user

    # Check if the user is making a POST request to update favorites
    if request.method == 'POST':
        form = FavoriteGolfersForm(request.POST)

        if form.is_valid():
            # Get the selected golfers
            selected_golfers = form.cleaned_data['golfers']

            # Update the user's favorite golfers (this clears previous selections)
            user.favorite_golfers.set(selected_golfers)
            user.save()

            # Redirect to a success page or the same page
            return redirect('update_favorite_golfers')  # Can redirect to a success page

    else:
        # Initialize the form with the user's current favorite golfers
        initial_golfers = user.favorite_golfers.all()
        form = FavoriteGolfersForm(initial={'golfers': initial_golfers})

    return render(request, 'update_favorites.html', {'form': form})


@login_required
def updatepage(request):
    return render(request, 'updatepage.html')  # Make sure 'blank.html' exists


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Optionally log them in right away
            return redirect('cars')  # Replace with your actual post-signup page
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form': form})