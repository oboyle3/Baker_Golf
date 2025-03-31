from django.urls import path
from . import views
from .views import login_view, logout_view
from .views import cars_view # Import the view function
urlpatterns = [
    
   
    path('cars/', cars_view, name='cars'),
   
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
]