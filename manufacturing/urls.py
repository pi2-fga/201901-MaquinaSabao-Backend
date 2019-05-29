from . import views
from django.urls import path


urlpatterns = [
    path(r'manufacturing/', views.ManufacturingCreateList.as_view()),
]