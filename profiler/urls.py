from django.urls import path
from profiler import views

app_name = "profiler"

urlpatterns = [
    path("criminal_profiles/", views.criminal_profiles, name="criminal_profiles"),
    path("criminal_profiles/add_profile/", views.add_profile, name="add_profile"),
    path(
        "criminal_profiles/profile/<int:criminal_id>/",
        views.view_profile,
        name="view_profile",
    ),
    path("criminal_profiles/match/", views.match_profile, name="match_profile"),
    path(
        "criminal_profiles/match/results/<int:match_id>/",
        views.match_results,
        name="match_results",
    ),
    path("search/", views.search, name="search"),
    path(
        "generate_results_pdf/<int:match_id>/",
        views.generate_results_pdf,
        name="generate_results_pdf",
    ),
]
