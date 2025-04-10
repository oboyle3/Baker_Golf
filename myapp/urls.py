from django.urls import path, include
from . import views
from .views import login_view, logout_view
from .views import cars_view # Import the view function
from .views import update_favorite_golfers
from .views import updatepage
from .views import signup_view
urlpatterns = [
    
   
    path('cars/', cars_view, name='cars'),
    path('update-favorites/', update_favorite_golfers, name='update_favorites'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('updatepage/', updatepage, name='updatepage'),
    path('signup/', signup_view, name='signup'),
    path('test/', views.test_view, name='test'),
    
]