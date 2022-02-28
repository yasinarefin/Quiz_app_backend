from django.urls import path, include
from Authentication import views
urlpatterns = [
    path('login/', views.login),
    path('logout/', views.logout),
]
