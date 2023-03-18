from django.urls import path
from contents.api import views

app_name = 'api_content'


urlpatterns = [
    path('content/', views.ContentDispatcherAPIView.as_view()),
    path('content/<pk>/', views.ContentDispatcherAPIView.as_view()),
]