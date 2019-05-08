from . import views
from django.urls import path


urlpatterns = [
    path(r'user/', views.UserCreateList.as_view()),
]