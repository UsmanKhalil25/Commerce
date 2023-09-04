from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Category(models.Model):
    title = models.CharField(max_length=64)

    def __str__(self):
        return self.title

class Bid(models.Model):
    bid = models.FloatField(default=0)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null =True, blank=True,related_name="bidUser")

    def __str__(self):
        return f"{self.bid}"



class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    price =models.ForeignKey(Bid,on_delete=models.CASCADE,null = True,blank=True,related_name="listingBid")
    isActive = models.BooleanField(default=True)
    img = models.CharField(max_length=1024)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null = True,blank = True,related_name="listingCategory")
    time = models.DateTimeField(default=timezone.now)
    watchlist = models.ManyToManyField(User,null =True,blank=True ,related_name="listingWatchlist")
    owner = models.ForeignKey(User,on_delete=models.CASCADE,null= True,blank=True,related_name="listingOwner" )

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField(default=timezone.now)
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE,blank=True,null=True,related_name="commentListing")
    def __str__(self):
        return f"Comment by {self.user.username}"