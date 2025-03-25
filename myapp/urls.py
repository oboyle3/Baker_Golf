from django.urls import path
from . import views
from .views import user_screen, car_list # Import the view function
urlpatterns = [
    #path('admin/', admin.site.urls),
    path('users/', views.user_list, name='user_list'),
    path('cars/', car_list, name='car-list'),
    path("user_screen/", user_screen, name="user_screen"),  # URL pattern
    # any other urls you want to define for your app
]