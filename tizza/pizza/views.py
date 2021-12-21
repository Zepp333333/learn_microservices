import json

from django.db.models import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.decorators import decorator_from_middleware

from .models import Pizza, Likes

from tizza.rate_limiter_middleware import RateLimit

rate_limit = decorator_from_middleware(RateLimit)


PIZZA_NOT_FOUND = json.dumps(
    {
        "status": "error",
        "message": "pizza not found"
    }
)


@login_required
def index(request, pid):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_pizza = Pizza.objects.create(
            title=data['title'],
            description=data['description'],
            creator=request.user,
        )
        new_pizza.save()
        content = content = {
            'id': new_pizza.id,
            'title': new_pizza.title,
            'description': new_pizza.description,
        }
        return HttpResponse(content=content)

    elif request.method == 'GET':
        try:
            pizza = Pizza.objects.get(id=pid)
        except ObjectDoesNotExist as _:
            return HttpResponse(PIZZA_NOT_FOUND)

        content = {
            'id': pizza.id,
            'title': pizza.title,
            'description': pizza.description,
        }
        json_content = json.dumps(content, indent=4)
        return HttpResponse(
            content=json_content
        )


@rate_limit
@login_required
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


@login_required
def like_pizza(request, pid):
    user = request.user
    pizza = Pizza.objects.get(id=pid)
    try:
        new_like = Likes.objects.create(user=user, pizza=pizza)
    except IntegrityError as e:
        print(e)
        return HttpResponse({'You have already liked this pizza.'})
    return HttpResponse({'Like recorded.'})


def dislike_pizza(request, pid):
    user = request.user
    pizza = Pizza.objects.get(id=pid)
    like = Likes.objects.filter(user=user, pizza=pizza).first()
    if like is None:
        return HttpResponse({"Like does not exist."})
    like.delete()
    return HttpResponse({"Dislike recorded."})
