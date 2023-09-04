from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import Http404

from .models import User,Listing,Category,Comment,Bid


def index(request):
    listing = Listing.objects.filter(isActive = True)
    return render(request, "auctions/index.html",{
        "listing":listing,
    })


def create(request):

    if request.method =="POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        img = request.POST.get("img")
        price = request.POST.get("price")
        categoryName = request.POST.get("category")
        category = Category.objects.get(title=categoryName)
        bid =Bid(bid = price,user = request.user)
        bid.save()
        listing = Listing(
            title = title,
            description = description,
            img= img,
            price = bid,
            owner= request.user,
            category = category
        )
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        allCategories = Category.objects.all()
        return render(request,"auctions/create.html",{
            "allCategories":allCategories
        })

def displayCategory(request, id):
    category = Category.objects.get(pk=id)
    listing = Listing.objects.filter(isActive=True, category=category)
    return render(request, "auctions/index.html", {
        "listing": listing
        })

def categories(request):
    categories = Category.objects.all()
    return render(request,"auctions/categories.html",{
        "categories":categories
    })

def listing(request,id):
    user = request.user
    listing = Listing.objects.get(pk = id)
    present = request.user in listing.watchlist.all()
    comments = Comment.objects.filter(listing  =listing)
    isOwner = user.username == listing.owner.username
    hasWon = user == listing.price.user and listing.isActive == False
    return render(request,"auctions/listing.html",{
        "listing":listing,
        "present":present,
        "comments":comments,
        "isOwner":isOwner,
        "hasWon":hasWon
    })

def addWatchlist(request,id):
    if request.method == "POST":
        listing = Listing.objects.get(pk = id)
        user = request.user
        listing.watchlist.add(user)
        return HttpResponseRedirect(reverse("listing", args=[id]))

def removeWatchlist(request,id):
    if request.method== "POST":
        listing = Listing.objects.get(pk = id)
        user = request.user
        listing.watchlist.remove(user)
        return HttpResponseRedirect(reverse("listing",args=[id]))
        

def watchlist(request):
    user = request.user
    listing = Listing.objects.filter(watchlist = user )
    return render(request,"auctions/watchlist.html",{
        "listing":listing
    })

def addComment(request,id):
    if request.method == "POST":
        comment =request.POST.get("comment")
        user = request.user
        listing = Listing.objects.get(pk = id)
        newComment = Comment(
            user =user,
            content = comment,
            listing = listing
            )
        
        newComment.save()
        return HttpResponseRedirect(reverse("listing",args=[id]))

def placeBid(request,id):
    if request.method == "POST":
        user = request.user
        price = request.POST.get("price")
        listing  =Listing.objects.get(pk = id)
        isOwner = user.username == listing.owner.username
        present = request.user in listing.watchlist.all()
        comments = Comment.objects.filter(listing  =listing)

        if listing.price.bid < float(price):
            newBid = Bid.objects.create(bid = price,user = user)
            newBid.save()
            listing.price = newBid
            listing.save()
            if isOwner == False and present ==False:
                listing.watchlist.add(user)
                present = True
                

            return render(request,"auctions/listing.html",{
                "listing":listing,
                "present":present,
                "comments":comments,
                "isOwner":isOwner,
                "bidPlaced":True
                    })
        else:
            return render(request,"auctions/listing.html",{
                "listing":listing,
                "present":present,
                "comments":comments,
                "isOwner":isOwner,
                "bidPlaced":False
                    })


def closeAuction(request, id):
    if request.method == "POST":
        user =request.user
        listing = Listing.objects.get(pk = id)
        listing.isActive = False
        listing.save()
        present = request.user in listing.watchlist.all()
        isOwner = user.username == listing.owner.username
        comments = Comment.objects.filter(listing = listing)
        return render(request,"auctions/listing.html",{
                "listing":listing,
                "present":present,
                "comments":comments,
                "isOwner":isOwner,
                "auctionClosed":True
                    })




        

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
