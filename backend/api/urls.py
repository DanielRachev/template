from django.urls import path
from .views import CreateUserView, ManageUserView

urlpatterns = [
    # User Management
    path("register/", CreateUserView.as_view(), name="create_user"),
    path("user/", ManageUserView.as_view(), name="manage_user"),
]
