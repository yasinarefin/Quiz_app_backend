from django.urls import path, include
from Quiz import views
urlpatterns = [
    path('view/<str:cur_status>/', views.show_quiz),
    path('questions/', views.questions),
    path('answers/', views.answers),
    path('participate/', views.participate),
    path('participation_status/', views.participation_status)
]