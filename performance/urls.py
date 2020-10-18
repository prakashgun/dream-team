from django.urls import path
from . import views

urlpatterns = [
    path('', views.CrawlInfoView.as_view(), name='crawl-info-view')
]
