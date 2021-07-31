from django.urls import path

from . import views


app_name='account'
urlpatterns = [
    path('logout/', views.Logout, name='logout'),
    # path('profile/', views.P.as_view(), name='profile'),
    path('change-password/', views.ChangePassword.as_view(), name='change_password'),
    
    path("activate/<slug:uidb64>/<slug:token>/", views.activate_email, name="activate"),

    path('reset/<uidb64>/<token>/', views.ResetPasswordVerify.as_view(), name='password_reset_confirm'),
]
