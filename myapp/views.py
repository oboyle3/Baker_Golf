from django.shortcuts import render
from .models import User, Golfer  # Import Golfer model

def user_list(request):
    users = User.objects.all()  # Get all users from the database
    golfers = Golfer.objects.all()  # Get all golfers from the database
    
    return render(request, 'users.html', {'users': users, 'golfers': golfers})  # Pass both users and golfers to the template
