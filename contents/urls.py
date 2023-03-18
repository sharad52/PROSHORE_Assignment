from django.urls import path
from contents import views


app_name = 'content'

urlpatterns = [
    path('', views.index, name='index'),
]