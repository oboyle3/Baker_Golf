from django.urls import path
from . import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('users/', views.user_list, name='user_list'),
    # any other urls you want to define for your app
]