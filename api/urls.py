from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    ChangePasswordView,
    ImageUploadView,
    LogoutAPIView,
    ProfileAPIView,
    RegisterAPIView,
    UpdateProfileAPIView,
    image_detail,
)

urlpatterns = [
    # user stuff CustomAuthToken
    path("login/", obtain_auth_token, name="login"),
    # path("login2/", CustomAuthToken.as_view(), name="login"),
    path("register/", RegisterAPIView.as_view(), name="register"),
    # profile
    path("profile/", ProfileAPIView.as_view(), name="profile"),
    # update profile
    path("update/<pk>/", UpdateProfileAPIView.as_view(), name="update"),
    # logout
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    # change password
    path(
        "change-password/",
        ChangePasswordView.as_view(),
        name="change-password",
    ),
    # upload image
    # path("upload-image/", ProfilePictureAPIView.as_view(), name="upload-image"),
    path("upload-images/", ImageUploadView.as_view(), name="image_upload"),
    # get images
    path("get-images/", image_detail, name="image_detail"),
    #
]
