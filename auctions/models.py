from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max
from django.core.exceptions import ValidationError

class User(AbstractUser):
    pass 

class Category(models.Model):
    name = models.CharField(max_length=64)

class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    starting_price = models.FloatField()
    description = models.CharField(max_length=512)
    is_active = models.BooleanField()
    category = models.ForeignKey(Category,on_delete=models.SET_NULL, null=True)
    photo = models.URLField(blank=True , default='')
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="listings")
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist")
    
    @property
    def current_price(self):
        return self.bid_set.aggregate(Max('price'))['price__max']
    
    @property
    def winner(self):
        if self.is_active:
            return None
        bids = self.bid_set.order_by('-price')
        return bids[0].bidder if bids else None
        

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.PROTECT , default=None)
    price = models.FloatField(default = 0.0)
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, default = None)
    
    def clean(self):
        if self.auction.current_price == None and self.price < self.auction.starting_price:
            raise ValidationError({'price': f"Value must be greater than or equal starting price: {self.auction.starting_price}!"})    
        elif self.auction.current_price != None and self.price <= self.auction.current_price:
            raise ValidationError({'price': f"Value must be greater than current price: {self.auction.current_price}!"})
        else:
            return self.price
             

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=256)
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)

