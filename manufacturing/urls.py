from . import views
from django.urls import path


urlpatterns = [
    path(r'manufacturing/', views.ManufacturingCreateList.as_view()),
    path('training_oil_quality/', views.training_oil_quality),
    path('predict_oil_quality/', views.predict_oil_quality),
    path('training_ph/', views.training_ph),
    path('predict_ph/', views.predict_ph),
    path('index_manufacturing_month/', views.index_manufacturing_month),
]
