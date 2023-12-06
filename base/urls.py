from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_criminal_case, name='add_criminal_case'),
    path('criminal-cases/', views.criminal_cases, name='criminal_cases'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/', views.user_register, name='user_register'),
    path('criminal/<str:case_number>/',
         views.CriminalDetailView.as_view(), name='criminal_detail'),
]
