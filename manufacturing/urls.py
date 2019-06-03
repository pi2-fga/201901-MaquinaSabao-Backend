from . import views
from django.urls import path


urlpatterns = [
    path(r'manufacturing/', views.ManufacturingCreateList.as_view()),
    path('training_oil_quality', views.training_oil_quality),
    path('predict_oil_quality', views.predict_oil_quality)
]