import uuid

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

    def generate_referral_code(self):
        return str(uuid.uuid4()).replace("-", "")[
            :10
        ]  # Generate a 10-character referral code

    # def save(self, *args, **kwargs):
    #     if not self.reffer_code:  # Check if referral code is not already set
    #         self.reffer_code = self.generate_referral_code()

    #     with transaction.atomic():
    #         # Save the NewUser instance first
    #         super().save(*args, **kwargs)

    #         if self.refferal:
    #             print("the refferal id ->", self.refferal)
    #             reffered_by = NewUser.objects.get(reffer_code=self.refferal)

    #             # Update the referrer's balance
    #             reffered_by.balance += 10
    #             reffered_by.save()

    #             # Create and save the RefferedModel instance
    #             RefferedModel.objects.create(
    #                 reffered_by=reffered_by, reffered_to=self, amount=0.5
    #             )

    #             # Update the current user's balance
    #             self.balance += 5
    #             self.save()

    def save(self, *args, **kwargs):
        if not self.reffer_code:  # Check if referral code is not already set
            self.reffer_code = self.generate_referral_code()
        if self.refferal:
            print("this is referred code -> ", self.refferal)
            reffered_by = NewUser.objects.get(reffer_code=self.refferal)
            reffered_by.balance += 10
            reffered_by.save()

            # Update this user balance
            self.balance += 5
            super(NewUser, self).save(*args, **kwargs)  # Save the instance first

            # Now add this to the referred model after the instance has been saved
            rm = RefferedModel.objects.create(
                reffered_by=reffered_by,
                reffered_to=self,
                amount=0.5,
                reffer_code=self.reffer_code,
            )
            rm.save()
        else:
            super(NewUser, self).save(
                *args, **kwargs
            )  # Save the instance without changes

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
    validity = models.IntegerField(default=7)

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
    package = models.ForeignKey(PackageModel, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0)
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
