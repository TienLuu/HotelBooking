from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import *


# Create your views here.


def index(request):
    return render(request, "Hotel/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "Hotel/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "Hotel/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "Hotel/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "Hotel/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "Hotel/register.html")


@login_required
def hotels(request):
    # if section == "all":
    #     posts = Post.objects.order_by("-timestamp").all()
    # elif section == "profile":
    #     posts = Post.objects.filter(
    #         user=request.user).order_by("-timestamp").all()
    # elif section == "following":
    #     posts = []
    #     for follower in request.user.followers.all():
    #         for post in Post.objects.filter(user=follower).order_by("-timestamp").all():
    #             posts.append(post)
    # else:
    #     return HttpResponse(status=404)
    # posts = posts.order_by("-timestamp").all()
    hotels = Hotel.objects.all()
    return JsonResponse([hotel.serialize() for hotel in hotels], safe=False)
