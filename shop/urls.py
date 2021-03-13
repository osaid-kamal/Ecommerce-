from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
path('', views.index, name="index"),
path('about/', views.about, name="about"),
path('contact/', views.contact, name="contact"),
path('tracker/', views.tracker, name="tracker"),
path('search/', views.search, name="search"),
path('productView/', views.productView, name="productView"),
path('checkout/', views.checkout, name="checkout"),
path('cart/', views.cart, name="cart"),
path('updateItem/', views.updateItem, name="updateItem"),
path('processOrder/', views.processOrder, name="processOrder"),
path('register/', views.register, name="register"),
path('logout/', views.logoutas, name="logoutas"),
path('login/', views.loginas, name="loginas"),
path("handlerequest/", views.handlerequest, name="HandleRequest"),


]