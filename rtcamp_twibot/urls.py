from django.urls import include, path
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('download/followers',views.export_csv,name="data_download"),
    path('download/tweets',views.export_csv_tweets,name="data_download"),
]