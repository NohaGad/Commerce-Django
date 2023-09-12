from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass 

class Category(models.Model):
    pass

class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    starting_price = models.FloatField()
    description = models.CharField(max_length=512)
    is_active = models.BooleanField()
    category = models.ForeignKey(Category,on_delete=models.SET_NULL, null=True)
    photo = models.URLField(blank=True , default='')
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="listings")
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist")
       

class Bid(models.Model):
    pass

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=256)
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)

