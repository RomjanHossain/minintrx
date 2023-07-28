from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    ChangePasswordView,
    EarnHistoryAPIView,
    ImageUploadView,
    LogoutAPIView,
    NotificationAPIView,
    PackageAPIView,
    PackagePurchaseAPIView,
    ProfileAPIView,
    QuizAPIView,
    RefferealCodeAPIView,
    RefferedUsersAPIView,
    RegisterAPIView,
    ScratchCardAPIView,
    SpinWheelAPIView,
    UpdateProfileAPIView,
    ViewWebsitesAPIView,
    WithdrawRequestApiView,
    WithdrowHistoryApiView,
    changeBalance,
    checkReffer,
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
    # chagne balance
    path("change_balance/", changeBalance, name="change_balance"),
    # check reffer code if exists then adding 10% of the users current balance
    path("check-reffer/", checkReffer, name="check-reffer"),
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
    # quiz views
    path("quiz/", QuizAPIView.as_view(), name="quiz"),
    # spin views
    path("spin/", SpinWheelAPIView.as_view(), name="spin"),
    # website views
    path("website/", ViewWebsitesAPIView.as_view(), name="website"),
    # scratch views
    path("scratch/", ScratchCardAPIView.as_view(), name="scratch"),
    # view all packages
    path("package/", PackageAPIView.as_view(), name="package"),
    # how and when the user earned
    path("earn/", EarnHistoryAPIView.as_view(), name="earn"),
    # package purchase views
    path(
        "package-purchase/", PackagePurchaseAPIView.as_view(), name="package-purchase"
    ),
    path("reffered/", RefferealCodeAPIView.as_view(), name="reffered"),
    # last 10 reffered users sort by ammount
    path("reffered-users/", RefferedUsersAPIView.as_view(), name="reffered-users"),
    path("notification/", NotificationAPIView.as_view(), name="notification"),
    # withdraw api
    path("withdraw/", WithdrawRequestApiView.as_view(), name="withdraw"),
    # withdraw history api
    # WithdrowHistoryApiView
    path(
        "withdraw-history/", WithdrowHistoryApiView.as_view(), name="withdraw-history"
    ),
]
