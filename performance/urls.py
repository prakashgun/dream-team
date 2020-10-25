from django.urls import path
from . import views

urlpatterns = [
    path('', views.CrawlInfoView.as_view(), name='crawl-info-view'),
    path('predict/', views.PredictView.as_view(), name='predict-view'),
    path('give-prediction/', views.GivePrediction.as_view(), name='give-prediction-view'),
]
