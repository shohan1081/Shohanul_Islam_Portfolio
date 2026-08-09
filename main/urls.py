from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('frontend/', views.frontend_detail, name='frontend'),
    path('backend/', views.backend, name='backend'),
    path('database/', views.database, name='database'),
    path('devops/', views.devops, name='devops'),
    path('software/', views.software, name= 'software'),
    path('contact/', views.contact_view, name='contact'),
    
]
