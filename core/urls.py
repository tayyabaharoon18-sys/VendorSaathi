from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('vendors/', views.vendors, name='vendors'),
    path('vendor/<int:id>/', views.vendor_detail, name='vendor_detail'),
    path('awareness/', views.awareness, name='awareness'),
    path('about/', views.about, name='about'),
    
    # Authentication URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
]

