import uuid
from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models


# New user model
class NewUser(AbstractUser):
    phone = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    refferal = models.CharField(max_length=50, blank=True, null=True)
    balance = models.FloatField(default=0.0)
    # reffer_code = models.UUIDField(default=uuid.uuid4, editable=False)
    reffer_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    mining_speed = models.FloatField(default=1.0)
    canWithdraw = models.BooleanField(default=False)
    # set withdraw start date
    withdraw_start_date = models.DateTimeField(blank=True, null=True)
    # minimum withdraw amount
    minimum_withdraw_amount = models.FloatField(default=0.0)
    # is reffered already
    is_reffered = models.BooleanField(default=False)

    # when saving,check if user is_reffered and the refferal code is point to a valid user, then increase the balance of the user by 10%
    def save(self, *args, **kwargs):
        if not self.is_reffered:
            try:
                user = NewUser.objects.get(reffer_code=self.refferal)
                user.balance += 0.1 * user.balance
                self.is_reffered = True
                user.save()
            except:
                pass
        super(NewUser, self).save(*args, **kwargs)

    def generate_referral_code(self):
        return str(uuid.uuid4()).replace("-", "")[
            :10
        ]  # Generate a 10-character referral code

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "Users"


# user profile image field
class ImageModel(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to="profile/")
    # user = models.CharField(max_length=50)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # user = Token.objects.get(key=self.user)
        # return self.user.username
        return self.user

    class Meta:
        verbose_name_plural = "Profile Picture"


# Quiz model
class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField(
        max_length=1000,
    )
    option1 = models.CharField(max_length=1000)
    option2 = models.CharField(max_length=1000)
    option3 = models.CharField(max_length=1000)
    option4 = models.CharField(max_length=1000)
    answer = models.CharField(max_length=1000)
    point = models.FloatField(default=0.0)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural = "Quiz"


# STATUS
SPIN_CHOICES = [
    ("Free", "Free"),
    ("Premium", "Premium"),
]


# Spin model
class Spin(models.Model):
    id = models.AutoField(primary_key=True)
    spin = models.CharField(max_length=1000)
    # win = models.CharField(max_length=1000)
    win_amount = models.FloatField(default=0.0)
    status = models.CharField(max_length=100, choices=SPIN_CHOICES, default="Free")

    def __str__(self):
        return self.spin

    class Meta:
        verbose_name_plural = "Spin"


# visit websites (list of websites)
class VisitWebsites(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=1000)
    condition = models.CharField(max_length=1000)
    thumbnail = models.ImageField(upload_to="thumbnail/")
    visit_ammount = models.FloatField(default=0.0)

    def __str__(self):
        return self.url

    class Meta:
        verbose_name_plural = "Visit Websites"


# scratch card
class ScratchCard(models.Model):
    id = models.AutoField(primary_key=True)
    scratch = models.CharField(max_length=1000)
    win_amount = models.FloatField(default=0.0)
    status = models.CharField(max_length=100, choices=SPIN_CHOICES, default="Free")

    def __str__(self):
        return self.scratch

    class Meta:
        verbose_name_plural = "Scratch Card"


# package model
class PackageModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    price = models.FloatField(default=0.0)
    mining_speed = models.FloatField(default=0.0)
    # validity = models.IntegerField(default=7)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Packages"


# Earned History
class EarnedHistory(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    amount = models.FloatField(default=0.0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Earned History"


# package purchase history

# STATUS
STATUS_CHOICE = [
    ("Pending", "Pending"),
    ("Approved", "Approved"),
    ("Declined", "Declined"),
]


class PackagePurchase(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    package_id = models.ForeignKey(PackageModel, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0)
    phone = models.CharField(max_length=1000)
    transaction_id = models.CharField(max_length=1000)
    transaction_type = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICE, default="Pending")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Package Purchase"


# reffer code where each reffer the user will get some amount
class RefferedModel(models.Model):
    id = models.AutoField(primary_key=True)
    # user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    reffer_code = models.CharField(max_length=1000)
    # reffered_user = models.ManyToManyField(NewUser, related_name="reffered_user")
    reffered_by = models.ForeignKey(
        NewUser, related_name="reffered_by", on_delete=models.CASCADE
    )
    reffered_to = models.ForeignKey(
        NewUser, related_name="reffered_to", on_delete=models.CASCADE
    )
    amount = models.FloatField(default=0.0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reffered_by.username

    class Meta:
        verbose_name_plural = "Reffered Code"


class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=1000)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Notification"


# withdrow request
class WithdrowRequest(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.FloatField(default=0.0)
    # phone = models.CharField(max_length=1000)
    address = models.CharField(max_length=1000)
    method = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICE, default="Pending")

    # def __str__(self):
    #     return self.user.username
    # if withdrow request is approved then the amount will be deducted from the user balance
    # and the amount will be added to the user withdrow history
    def save(self, *args, **kwargs):
        if self.status == "Approved":
            user = NewUser.objects.get(username=self.user)
            user.balance = user.balance - self.amount
            user.save()
            WithdrowHistory.objects.create(
                user=self.user, amount=self.amount, method=self.method
            )
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Withdrow Request"


class WithdrowHistory(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0)
    method = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Withdrow History"


# Withdraw status on/off
WITHDRAW_STATUS = [
    ("On", "On"),
    ("Off", "Off"),
]


# withdraw on/off, minimum withdraw date and minimum withdraw amount
class WithdrawSetting(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=100, choices=WITHDRAW_STATUS, default="Off")
    minimum_withdraw_amount = models.FloatField(default=0.0)
    # minimum_withdraw_date = models.IntegerField(default=7)
    # minimum withdraw date is a date field , default is 7 days from the date of withdraw
    minimum_withdraw_date = models.DateField(
        default=datetime.today() + timedelta(days=7)
    )

    # when saving this model then all the users can withdraw set true/false depending on the status, minimum withdraw amount and minimum withdraw date
    def save(self, *args, **kwargs):
        if self.status == "On":
            users = NewUser.objects.all()
            for user in users:
                user.canWithdraw = True
                user.save()
        else:
            users = NewUser.objects.all()
            for user in users:
                user.canWithdraw = False
                user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name_plural = "Withdraw Setting"
