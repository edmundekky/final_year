from django.urls import path, include
from accounts import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path(
        "investigator_profile/", views.investigator_profile, name="investigator_profile"
    ),
    path("login/", views.investigator_login, name="login"),
    path("logout/", views.investigator_logout, name="logout"),
    path(
        "password_change/", views.investigator_password_change, name="password_change"
    ),
    path(
        "update_investigator_profile/",
        views.update_investigator_profile,
        name="update_investigator_profile",
    ),
    path(
        "add_investigator/",
        views.add_investigator,
        name="add_investigator",
    ),
    path(
        "investigators/",
        views.review_investigators,
        name="review_investigators",
    ),
    path("contact/", views.contact, name="contact"),
    path(
        "password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
