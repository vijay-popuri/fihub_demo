from django.contrib import admin
from django.urls import path
from ftapp import views

urlpatterns = [
    path('',  views.home, name='home'),
    path('cart', views.cart, name='cart'),
    path('rem', views.rem, name='rem'),
    path('remitem', views.remitem, name='remitem'),
    path('buy', views.buy, name='buy'),
    path('myorders', views.myorders, name='myorders'),
    path('contact', views.contact, name='contact'),
    path('clearorder', views.clearorder, name='clearorder'),
    path('cartg/', views.cartg, name='cartg'),
    path('login/',  views.login, name='login'),
    path('logvalid',  views.logvalid, name='logvalid'),
    path('prod/', views.prod, name='prod'),
    path('work/', views.work, name='work'),
    path('reg/',  views.reg, name='reg'),
    path('regsave',  views.regsave, name='regsave'),
]