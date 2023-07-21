from api.serializations import (
    ChangePasswordSerializer,
    EarnedHistorySerializer,
    ImageSerializer,
    NewUserSerializer,
    NotificationSerializer,
    PackagePurchaseSerializer,
    PackageSerializer,
    QuizSerializer,
    ReffereSerializer,
    ScratchCardSerializer,
    SpinSerializer,
    UpdateUserSerializer,
    VisitWebsitesSerializer,
)
from django.contrib.auth import update_session_auth_hash
from landing.models import (
    EarnedHistory,
    ImageModel,
    NewUser,
    Notification,
    PackageModel,
    PackagePurchase,
    Quiz,
    RefferedModel,
    ScratchCard,
    Spin,
    VisitWebsites,
)
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
)


# register the user
class RegisterAPIView(CreateAPIView):
    queryset = NewUser.objects.all()
    model = NewUser()
    serializer_class = NewUserSerializer


# get the user profile
class ProfileAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NewUserSerializer

    def get_queryset(self):
        return NewUser.objects.filter(id=self.request.user.id)

    def get(self, request, *args, **kwargs):
        return Response(self.get_queryset().values()[0])


# update the user profile
class UpdateProfileAPIView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer

    def get_queryset(self):
        return NewUser.objects.filter(id=self.request.user.id)

    def get_object(self):
        pk = self.kwargs["pk"]
        queryset = self.get_queryset()
        obj = queryset.get(pk=pk)
        return obj

    def put(self, request, *args, **kwargs):
        # queryset = self.get_queryset().first()
        queryset = self.get_object()
        serializer = self.get_serializer(
            queryset,
            data=request.data,
            partial=True,
        )
        # serializer = self.get_serializer(
        #     queryset, data=request.data, partial=True, many=True
        # )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# logout the user
class LogoutAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NewUserSerializer

    def get_queryset(self):
        return NewUser.objects.filter(id=self.request.user.id)

    def get(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response({"message": "User logged out successfully"}, status=HTTP_200_OK)


class ChangePasswordView(UpdateAPIView):
    model = NewUser
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            update_session_auth_hash(request, self.object)
            return Response("Success.", status=HTTP_200_OK)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# get image detail
@api_view(["GET"])
def image_detail(request):
    try:
        # image = ImageModel.objects.get(pk=pk)
        # get image using user
        _image = ImageModel.objects.filter(user=request.user.id)
        print("this is user id -> ", request.user.id)
    except ImageModel.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ImageSerializer(_image, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


# upload image
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def image_upload(request):
    # only allow authenticated users to upload images

    if request.method == "POST":
        _user = request.user
        _image = request.FILES.get("image")
        serializer = ImageSerializer(data={"user": _user, "image": _image})
        print("this is image -> ", _image)
        print("this is user -> ", _user)
        # serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    # get method is not allowed
    return Response(status=HTTP_405_METHOD_NOT_ALLOWED)


# convert that image_upload function into a class based view
class ImageUploadView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ImageSerializer

    def post(self, request, *args, **kwargs):
        # get user id
        # get user field data
        # _user = request.data.get("user")
        print("this is user -> ", request.user.id)
        _image = request.FILES.get("image")
        print("this is image -> ", _image)
        serializer = self.get_serializer(
            data={"user": request.user.id, "image": _image}
        )
        if serializer.is_valid():
            # check if user has already uploaded an image
            if ImageModel.objects.filter(user=request.user.id).exists():
                # delete the previous image
                ImageModel.objects.filter(user=request.user.id).delete()
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# upload the user profile picture and get the user profile picture
class ProfilePictureAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ImageSerializer
    model = ImageModel()

    def get_queryset(self):
        return ImageModel.objects.filter(user=self.request.user)

    # def get_queryset(self):
    #     return NewUser.objects.filter(id=self.request.user.id)

    def get_object(self):
        pk = self.kwargs["pk"]
        queryset = self.get_queryset()
        obj = queryset.get(pk=pk)
        return obj

    def get(self, request, *args, **kwargs):
        queryset = self.get_object()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        queryset = self.get_object()
        serializer = self.get_serializer(
            queryset,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        queryset = self.get_object()
        queryset.profile_picture.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        print("post method called in new CustomAuthToken")
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


# Quiz API Views
class QuizAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()[:10]


# Spin Wheel API Views
class SpinWheelAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SpinSerializer
    queryset = Spin.objects.all()[:10]


# View websites
class ViewWebsitesAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = VisitWebsitesSerializer
    queryset = VisitWebsites.objects.all()


# scratch card view
class ScratchCardAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ScratchCardSerializer
    queryset = ScratchCard.objects.all()[:10]


# package view
class PackageAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PackageSerializer
    queryset = PackageModel.objects.all()


# earn history view
class EarnHistoryAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EarnedHistorySerializer

    # queryset will be filtered by user id
    def get_queryset(self):
        return EarnedHistory.objects.filter(user=self.request.user)


# package purchase view
class PackagePurchaseAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PackagePurchaseSerializer

    # queryset = PackagePurchase.objects.all()
    def get_queryset(self):
        return PackagePurchase.objects.filter(user=self.request.user)


# refferal code view
class RefferealCodeAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReffereSerializer

    # queryset = PackagePurchase.objects.all()
    def get_queryset(self):
        return RefferedModel.objects.filter(user=self.request.user)


# get 10 reffered users sort by ammount (api view only)
class RefferedUsersAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReffereSerializer

    # queryset = PackagePurchase.objects.all()
    def get_queryset(self):
        return RefferedModel.objects.filter(user=self.request.user).order_by("-amount")[
            :10
        ]


class NotificationAPIView(ListAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer

    # def get_queryset(self):
    #     return Notification.objects.filter(user=self.request.user)
    # get the last notifications
    def get_queryset(self):
        return Notification.objects.all().order_by("-id")[-1]
