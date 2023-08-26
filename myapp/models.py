from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    icon = models.ImageField(
        verbose_name="画像", upload_to="uploads", default="image/noimage.png"
    )

class Talk(models.Model):
    talk =  models.CharField(max_length=500)
    talk_from = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="talk_from"
    )
    talk_to= models.ForeignKey(User, on_delete=models.CASCADE, related_name="talk_to")
    time = models.DateTimeField(auto_now_add=True)
