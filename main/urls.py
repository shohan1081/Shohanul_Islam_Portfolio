from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('frontend/', views.frontend_detail, name='frontend'),
    path('backend/', views.backend, name='backend'),
    path('database/', views.database, name='database'),
    path('desktop/', views.desktop, name='desktop'),
    path('software/', views.software, name= 'software'),
    path('contact/', views.contact_view, name='contact'),
    
]
