from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home),
    path('objekty', views.Objekty),
    path('fotogalerie/<str:url>', views.Galerie),
    path('fotogalerie/<str:url1>/<str:url2>', views.GalerieViews),
    path('historie/<str:url>', views.Historie),
    path('<str:url>', views.Error),
]