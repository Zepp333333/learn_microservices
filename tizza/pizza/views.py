from django.shortcuts import render

from django.http import HttpResponse
from .models import Pizza, Likes
import json
from django.db.models import ObjectDoesNotExist


def index(request, pid):
    try:
        pizza = Pizza.objects.get(id=pid)
    except ObjectDoesNotExist as _:
        return HttpResponse(
            json.dumps(
                {
                    "status": "error",
                    "message": "pizza not found"
                }
            )
        )

    print(request.user)
    content = {
        'id': pizza.id,
        'title': pizza.title,
        'description': pizza.description,
    }
    json_content = json.dumps(content, indent=4)
    return HttpResponse(
        content=json_content
    )


def random(request):
    liked_pizza_ids = Likes.objects.filter(user=request.user.id).values('pizza_id')
    unseen_pizzas = Pizza.objects.exclude(id__in=liked_pizza_ids).order_by('?')[:15]

    if not unseen_pizzas:
        return HttpResponse(
            json.dumps(
                {
                    "status": "error",
                    "message": "no unseen pizzas found"
                }
            )
        )

    content = [
        {'id': pizza.id,
         'title': pizza.title,
         'description': pizza.description}
        for pizza in unseen_pizzas
    ]

    return HttpResponse(json.dumps(content))
