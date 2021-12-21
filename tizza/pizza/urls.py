from django.urls import include, path
from .views import index, random

urlpatterns = [
    path('<int:pid>', index, name='pizza'),
    path('random/', random, name='ramdom_pizzas')
]
