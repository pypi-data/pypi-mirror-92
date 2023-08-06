from django.urls import path

from . import views

app_name = "permission"

urlpatterns = [
    path("users/permissions/", views.ModuleView.as_view()),

]
