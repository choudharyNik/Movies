from django.urls import path
from movies import views

urlpatterns = [
    path('getcreate/', views.list_or_create_movie),
    path('movies/<int:id>/', views.retrieve_update_delete_movie),
]