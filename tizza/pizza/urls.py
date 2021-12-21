from django.urls import include, path
from .views import index, random, like_pizza, dislike_pizza

urlpatterns = [
    path('<int:pid>', index, name='pizza'),
    path('random/', random, name='random_pizzas'),
    path('like/<int:pid>', like_pizza, name='like_pizza'),
    path('dislike/<int:pid>', dislike_pizza, name='dislike_pizza'),
]
