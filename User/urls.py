from django.urls import path, include
from User import views
urlpatterns = [
    path('create_user/', views.create_user),
    path('get_user/', views.get_user),
]
