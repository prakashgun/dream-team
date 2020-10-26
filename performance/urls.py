from django.urls import path
from . import views

urlpatterns = [
    path('crawl-info/', views.CrawlInfoView.as_view(), name='crawl-info-view'),
    path('save-model/', views.SaveModelView.as_view(), name='save-model-view'),
    path('predict/', views.PredictView.as_view(), name='predict-view'),
]
