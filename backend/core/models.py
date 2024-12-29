from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User



class CustomUser(AbstractUser):
    # is_active = models.BooleanField(default=False)  # Can only be set by admin

    def __str__(self):
        return self.username

class Image(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/project/")
    description = models.TextField()
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.description


class ServiceImage(models.Model):
    icon = models.ImageField(upload_to="images/services/")
    service = models.CharField(max_length=50)
    feature = models.TextField()

    def __str__(self):
        return self.service



class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    verification_code = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username


