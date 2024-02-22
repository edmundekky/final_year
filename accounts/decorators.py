# decorators.py
from django.shortcuts import redirect
from django.contrib import messages


def investigator_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            # User is authenticated allow access to the view.
            return view_func(request, *args, **kwargs)
        else:
            # User is not authenticated, redirect to the homepage view.
            messages.error(
                request,
                "You need to login to access this page. If you don't have an account, please sign up.",
            )
            return redirect("login")

    return wrapper


def guest_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # User is not authenticated (guest user), allow access to the view.
            return view_func(request, *args, **kwargs)
        elif request.user.is_authenticated:
            # User is authenticated and is a parent, redirect to the parent dashboard view.
            messages.error(
                request,
                "You are already logged in. If you want to access the previous page, please log out first.",
            )
            return redirect("dashboard")

    return wrapper
