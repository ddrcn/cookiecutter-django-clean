from django.urls import path
from .views.web import home  # Example: import view

app_name = "users"
urlpatterns = [
    path("", home, name="home"),
]
