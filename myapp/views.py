from django.shortcuts import render, redirect
from .models import User, Golfer , AllUsersFavoriteGolfers, UserAverage
from django.contrib.auth import authenticate, login, logout
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



# @login_required
# def test_view(request):
#     # Filter the table by logged-in user
#     favorite_entries = AllUsersFavoriteGolfers.objects.filter(user=request.user).select_related('golfer')

#     context = {
#         'favorites': favorite_entries
#     }

#     return render(request, 'test.html', context)
# @login_required
# def test_view(request):
#     # Get all golfers and group them by tier
#     golfers = Golfer.objects.all()
#     golfers_by_tier = golfers.order_by('tier')  # Order golfers by tier
#     golfers_by_tier = [
#         (tier, golfers.filter(tier=tier)) for tier in golfers.values_list('tier', flat=True).distinct()
#     ]
    
#     # Get the current favorite golfers for the user
#     current_favorites = AllUsersFavoriteGolfers.objects.filter(user=request.user)
#     selected_golfers = [entry.golfer.id for entry in current_favorites]

#     # Handle form submission to update favorites
#     if request.method == 'POST':
#         # Get selected golfers from the form (one per tier)
#         selected_golfers_from_form = {
#             key.split('_')[1]: value
#             for key, value in request.POST.items()
#             if key.startswith('tier_')
#         }
        
#         # Remove all current favorite golfers for the user
#         AllUsersFavoriteGolfers.objects.filter(user=request.user).delete()
        
#         # Add the new selected golfers to the user's favorites
#         for tier, golfer_id in selected_golfers_from_form.items():
#             golfer = Golfer.objects.get(id=golfer_id)
#             AllUsersFavoriteGolfers.objects.create(user=request.user, golfer=golfer)

#         return redirect('cars')  # Redirect to refresh the page with the updated favorites

#     context = {
#         'favorites': current_favorites,
#         'golfers_by_tier': golfers_by_tier,
#         'selected_golfers': selected_golfers,
#     }

#     return render(request, 'test.html', context)
# @login_required
# def test_view(request):
#     # Get all golfers and group them by tier
#     golfers = Golfer.objects.all()
#     golfers_by_tier = golfers.order_by('tier')  # Order golfers by tier
#     golfers_by_tier = [
#         (tier, golfers.filter(tier=tier)) for tier in golfers.values_list('tier', flat=True).distinct()
#     ]
    
#     # Get the current favorite golfers for the user
#     current_favorites = AllUsersFavoriteGolfers.objects.filter(user=request.user)
#     selected_golfers = [entry.golfer for entry in current_favorites]

#     # Handle form submission to update favorites
#     if request.method == 'POST':
#         # Get selected golfers from the form (one per tier)
#         selected_golfers_from_form = {
#             key.split('_')[1]: value
#             for key, value in request.POST.items()
#             if key.startswith('tier_')
#         }
        
#         # Remove all current favorite golfers for the user
#         AllUsersFavoriteGolfers.objects.filter(user=request.user).delete()
        
#         # Add the new selected golfers to the user's favorites
#         for tier, golfer_id in selected_golfers_from_form.items():
#             golfer = Golfer.objects.get(id=golfer_id)
#             AllUsersFavoriteGolfers.objects.create(user=request.user, golfer=golfer)

#         # Redirect to the cars page after updating
#         return redirect('cars')

#     # Add average over par calculation for selected golfers
#     golfers_with_avg_over_par = [
#         {'golfer': golfer, 'avg_over_par': golfer.calculate_average_over_par()} for golfer in selected_golfers
#     ]
    
#     context = {
#         'favorites': current_favorites,
#         'golfers_by_tier': golfers_by_tier,
#         'selected_golfers': selected_golfers,
#         'golfers_with_avg_over_par': golfers_with_avg_over_par,  # Pass the calculated averages
#     }

#     return render(request, 'test.html', context)

@login_required
def test_view(request):
    # Get all golfers and group them by tier
    golfers = Golfer.objects.all()
    golfers_by_tier = golfers.order_by('tier')  # Order golfers by tier
    golfers_by_tier = [
        (tier, golfers.filter(tier=tier)) for tier in golfers.values_list('tier', flat=True).distinct()
    ]
    
    # Get the current favorite golfers for the user
    current_favorites = AllUsersFavoriteGolfers.objects.filter(user=request.user)
    selected_golfers = [entry.golfer for entry in current_favorites]

    # Handle form submission to update favorites
    if request.method == 'POST':
        # Get selected golfers from the form (one per tier)
        selected_golfers_from_form = {
            key.split('_')[1]: value
            for key, value in request.POST.items()
            if key.startswith('tier_')
        }
        
        # Remove all current favorite golfers for the user
        AllUsersFavoriteGolfers.objects.filter(user=request.user).delete()
        
        # Add the new selected golfers to the user's favorites
        for tier, golfer_id in selected_golfers_from_form.items():
            golfer = Golfer.objects.get(id=golfer_id)
            AllUsersFavoriteGolfers.objects.create(user=request.user, golfer=golfer)

        # Redirect to the same page after updating
        return redirect('test_view')

    # Add average over par calculation for selected golfers
    golfers_with_avg_over_par = [
        {'golfer': golfer, 'avg_over_par': golfer.calculate_average_over_par()} for golfer in selected_golfers
    ]
    
    # Calculate the overall average over par for the selected golfers
    valid_averages = [item['avg_over_par'] for item in golfers_with_avg_over_par if item['avg_over_par'] is not None]
    overall_avg_over_par = None
    if valid_averages:
        overall_avg_over_par = sum(valid_averages) / len(valid_averages)

    # Save the overall average to UserAverage model
    user_average, created = UserAverage.objects.get_or_create(user=request.user)
    user_average.overall_avg_over_par = overall_avg_over_par
    user_average.save()

    context = {
        'favorites': current_favorites,
        'golfers_by_tier': golfers_by_tier,
        'selected_golfers': selected_golfers,
        'golfers_with_avg_over_par': golfers_with_avg_over_par,
        'overall_avg_over_par': overall_avg_over_par,  # Pass the overall average over par
    }

    return render(request, 'test.html', context)

@login_required
def leaderboard_view(request):
    # Fetch UserAverage entries and join with the related User objects
    leaderboard = UserAverage.objects.select_related('user').order_by('overall_avg_over_par')

    context = {
        'leaderboard': leaderboard,
    }
    return render(request, 'leaderboard.html', context)