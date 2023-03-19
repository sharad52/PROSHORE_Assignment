from django.urls import path
from contents import views


app_name = 'content'

urlpatterns = [
    path('', views.ContentListView.as_view(), name='list_content'),
    path('content/', views.ContentView.as_view(), name='save_content'),
    path('content/<pk>/', views.ContentView.as_view(), name='view_content'),
]