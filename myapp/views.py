from django.shortcuts import render
from .models import User, Golfer  # Import Golfer model
from django.shortcuts import render, get_object_or_404

def user_list(request):
    users = User.objects.all()  # Get all users from the database
    golfers = Golfer.objects.all()  # Get all golfers from the database
    users_with_golfers = User.objects.prefetch_related('usergolfer_set')
    
    return render(request, 'users.html', {'users': users, 'golfers': golfers, 'users_with_golfers': users_with_golfers})  # Pass both users and golfers to the template


def user_screen(request):
    return render(request, "user_screen.html")  # This loads your template



def users_page(request):
    return render(request, "users.html")  # This loads users.html




def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'user_screen.html', {'user': user})
