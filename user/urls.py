from django.urls import path

from user.views import CreateUserView, ManagerUserView

app_name = 'user'

urlpatterns = [
    path("", CreateUserView.as_view(), name="register"),
    path("me/", ManagerUserView.as_view(), name="manage"),
]