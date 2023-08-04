from django.contrib.auth.password_validation import validate_password
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
    WithdrowRequest,
)
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


# New user serializer
class NewUserSerializer(ModelSerializer):
    def create(self, validated_data):
        # cleaned the data
        cleaned_data = self.validate(validated_data)
        # create the user
        user = NewUser.objects.create_user(
            username=cleaned_data["username"],
            email=cleaned_data["email"],
            password=cleaned_data["password"],
            phone=cleaned_data["phone"],
            first_name=cleaned_data["first_name"],
            last_name=cleaned_data["last_name"],
            country=cleaned_data["country"],
            refferal=cleaned_data["refferal"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validate(self, data):
        if NewUser.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError("Email already exists")
        if NewUser.objects.filter(username=data["phone"]).exists():
            raise serializers.ValidationError("Phone already exists")
        if len(data["password"]) < 6:
            raise serializers.ValidationError("Password too short")
        if NewUser.objects.filter(username=data["username"]).exists():
            raise serializers.ValidationError("Username already exists")

        return data

    class Meta:
        model = NewUser
        # fields = "__all__"
        fields = (
            "email",
            "password",
            "first_name",
            "last_name",
            "phone",
            "username",
            "country",
            "refferal",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "phone": {"required": True},
            "email": {"required": True},
            "country": {"required": True},
            "refferal": {"required": True},
        }


# change balance serializer
class ChangeBalanceSerializer(ModelSerializer):
    def update(self, instance, validated_data):
        instance.balance = instance.balance + validated_data.get("balance", 0)
        instance.save()
        return instance

    class Meta:
        model = NewUser
        fields = ("balance",)


# Update user serializer
class UpdateUserSerializer(ModelSerializer):
    class Meta:
        model = NewUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone",
            "username",
            "password",
        )

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.username = validated_data.get("username", instance.username)
        # add the new balance to the old balance
        instance.balance = instance.balance + validated_data.get("balance", 0)
        instance.save()
        return instance


# ChangePasswordSerializer
class ChangePasswordSerializer(ModelSerializer):
    model = NewUser
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

    # def validate(self, data):
    #     user = self.context["request"].user
    #     if not user.check_password(data["old_password"]):
    #         raise serializers.ValidationError("Wrong password")
    #     return data

    # def update(self, instance, validated_data):
    #     instance.set_password(validated_data["new_password"])
    #     instance.save()
    #     return instance

    class Meta:
        model = NewUser
        fields = ("old_password", "new_password")


# check reffer serializer
class CheckRefferSerializer(ModelSerializer):
    # check if the refferal code exists then if it exists then check how many RefferedModel objects are there with the same refferal code
    # add the balance to the user multiplied by the number of RefferedModel objects
    def update(self, instance, validated_data):
        # get the refferal code
        refferal = validated_data.get("refferal", None)
        # get the user
        user = instance
        # check if the refferal code exists
        if NewUser.objects.filter(reffer_code=refferal).exists():
            # get the user with the refferal code
            reffered_by = NewUser.objects.get(reffer_code=refferal)
            # get the number of RefferedModel objects with the same refferal code
            reffered_model = RefferedModel.objects.filter(reffer_code=refferal)
            # get the number of RefferedModel objects
            reffered_model_count = reffered_model.count()
            # get the amount
            amount = reffered_model_count * 0.5
            # add the balance to the user
            reffered_by.balance += amount
            # save the user
            reffered_by.save()
            # add 10% of the users current balance
            user.balance += user.balance * 0.1
            # save the user
            user.save()
            # create the RefferedModel object
            reffered_model = RefferedModel.objects.create(
                reffered_by=reffered_by,
                reffered_to=user,
                amount=amount,
                reffer_code=refferal,
            )
            # save the RefferedModel object
            reffered_model.save()
        return instance

    class Meta:
        model = NewUser
        fields = ("refferal",)


# image serializer
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        # fields = ("image",)
        fields = "__all__"


# quiz serializer
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = "__all__"


# spin serializer
class SpinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spin
        fields = "__all__"


# visit websites serializer
class VisitWebsitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitWebsites
        fields = "__all__"


# scratch card serializer
class ScratchCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScratchCard
        fields = "__all__"


# package serializer
class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageModel
        fields = "__all__"


# earned history serializer
class EarnedHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EarnedHistory
        fields = "__all__"


# package purchase serializer
class PackagePurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackagePurchase
        fields = "__all__"


# reffered serializer
class ReffereSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefferedModel
        fields = "__all__"


# notification serializer
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"


class WithdrowReqeustSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrowRequest
        fields = "__all__"
