from django.urls import path
from . import views
from .views import login_view, logout_view
from .views import cars_view # Import the view function
from .views import update_favorite_golfers
urlpatterns = [
    
   
    path('cars/', cars_view, name='cars'),
    path('update-favorites/', update_favorite_golfers, name='update_favorites'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
]