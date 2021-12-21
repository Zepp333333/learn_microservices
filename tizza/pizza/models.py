from django.db import models

from django.contrib.auth.models import User


class Pizzeria (models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=512)
    phone = models.CharField(max_length=40)


class Pizza(models.Model):
    TYPES = [
        (1, 'Meat'),
        (2, 'Vegeterian'),
        (3, 'Vegan'),
    ]

    title = models.CharField(max_length=120)
    description = models.CharField(max_length=240)
    thumbnail_url = models.URLField()
    approved = models.BooleanField(default=False)
    creator = models.ForeignKey(Pizzeria, on_delete=models.CASCADE)
    pizza_type = models.IntegerField(choices=TYPES, default=1)


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
