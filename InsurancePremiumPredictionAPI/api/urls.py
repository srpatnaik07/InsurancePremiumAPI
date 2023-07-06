from django.urls import path
from .views import PremiumPrediction

urlpatterns = [
    path('expenses/',PremiumPrediction.as_view(),name='Insurance_Premium_Prediction')
]