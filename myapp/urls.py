from django.urls import path
from . import views
from .views import login_view, logout_view
from .views import cars_view # Import the view function
urlpatterns = [
    #path('admin/', admin.site.urls),
   # path('users/', views.user_list, name='user_list'),
    path('cars/', cars_view, name='cars'),
   # path("user_screen/", user_screen, name="user_screen"),  # URL pattern
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    # any other urls you want to define for your app
]