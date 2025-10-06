from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='login_user'),
    path('home/', views.home, name='home'),
    path('register/', views.register_user, name='register_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('save_prediction/', views.save_prediction, name='save_prediction'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('get-latest-profile/', views.get_latest_profile, name='get_latest_profile'),
    
    # --- THIS IS THE FIX ---
    # This path is for the quick history pop-up on the main page.
    path('fetch-history/', views.fetch_history, name='fetch_history'),
    
    # This path is for the full, separate archive page.
    path('archive/', views.archive, name='archive'),
]