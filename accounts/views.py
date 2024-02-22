from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import redirect, render

from accounts.decorators import guest_required, investigator_required
from accounts.models import Contact, Investigator, ContactType

from .forms import InvestigatorForm, ContactForm
from profiler.models import CyberCriminal


@investigator_required
def dashboard(request):
    investigator = request.user
    cyber_criminals = CyberCriminal.objects.all()
    investigators = Investigator.objects.all()

    template_name = "dashboard.html"
    context = {
        "investigator": investigator,
        "cyber_criminals": cyber_criminals,
        "recent_cyber_criminals": cyber_criminals[:5],
        "investigators": investigators,
    }
    return render(request, template_name, context)


@investigator_required
def investigator_profile(request):
    investigator = request.user

    template_name = "accounts/investigator_profile.html"
    context = {"investigator": investigator}
    return render(request, template_name, context)


@guest_required
def investigator_login(request):
    if request.method == "POST":
        # Handle login form submission.
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            # Authenticate the user.
            investigator = authenticate(username=username, password=password)
            if investigator is not None:
                # investigator is authenticated, log them in.
                login(request, investigator)
                messages.success(request, f"Welcome back {investigator.username}!")
                return redirect("dashboard")
            else:
                # investigator is not authenticated, display error message.
                messages.error(
                    request, "Invalid username or password. Please try again."
                )
        else:
            messages.error(request, "Invalid form data. Please check your inputs.")
        return redirect("login")

    template_name = "accounts/login.html"
    context = {}
    return render(request, template_name, context)


def investigator_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("login")


@investigator_required
def investigator_password_change(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)  # Add this line
            messages.success(request, "Your password has been changed successfully.")
        else:
            messages.error(request, "Invalid form data. Please check your inputs.")

    return redirect("investigator_profile")


@investigator_required
def update_investigator_profile(request):
    investigator = request.user

    if request.method == "POST":
        investigator.first_name = request.POST.get("first_name")
        investigator.last_name = request.POST.get("last_name")
        investigator.email = request.POST.get("email")
        investigator.phone = request.POST.get("phone")
        investigator.address = request.POST.get("address")
        investigator.save()

        messages.success(request, "Your profile has been updated successfully.")
    else:
        messages.error(request, "Invalid access method.")
    return redirect("investigator_profile")


@investigator_required
def add_investigator(request):
    if request.method == "POST":
        form = InvestigatorForm(request.POST)
        if form.is_valid():
            investigator = form.save(commit=False)
            investigator.set_password(form.cleaned_data.get("password1"))
            investigator.save()
            messages.success(request, "Investigator has been added successfully.")
        else:
            messages.error(
                request, f"Invalid form data. Please check your inputs. {form.errors}"
            )
            return redirect("add_investigator")

    template_name = "accounts/add_investigator.html"
    context = {}
    return render(request, template_name, context)


@investigator_required
def review_investigators(request):
    investigators = Investigator.objects.all()

    template_name = "accounts/review_investigators.html"
    context = {"investigators": investigators}
    return render(request, template_name, context)


def contact(request):
    if request.method != "POST":
        contact_form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_form = form.save(commit=False)
            if request.user.is_authenticated:
                contact_form.name = request.user.get_full_name()
                contact_form.email = request.user.email
                contact_form.contact_type = ContactType.INVESTIGATOR
            else:
                name = request.POST.get("name")
                email = request.POST.get("email")
                contact_form.name = name
                contact_form.email = email

            contact_form.save()

        messages.success(request, "Your message has been sent successfully.")
        if request.user.is_authenticated:
            return redirect("dashboard")
        else:
            return redirect("home")

    template_name = "accounts/contact.html"
    context = {"contact_form": contact_form, "section": "contact"}
    return render(request, template_name, context)
