from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    start_bid = models.FloatField()
    url_pic = models.URLField(max_length=500)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="owner",to_field='username')
    status = models.CharField(max_length=10,default="Open")

    def __str__(self):
        return f"{self.id}"
    
class User(AbstractUser):
    watchlist = models.ManyToManyField(Listing,blank=True,related_name="watchers")

class Bid(models.Model):
    item = models.ForeignKey(Listing,on_delete=models.CASCADE, related_name="item_id")
    bid = models.FloatField()
    uname = models.ForeignKey(User,on_delete=models.CASCADE,related_name="uname")

    def __str__(self):
        return f"${self.bid} by {self.uname} for {self.item_id}"


class Comment(models.Model):
    username = models.ForeignKey(User,on_delete=models.CASCADE,related_name="commentUser")

    itemID = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="itemID")

    text = models.CharField(max_length=500)

