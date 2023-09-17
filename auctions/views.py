from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionListing, Category

class NewAuctionForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.Textarea(attrs={'placeholder':'Title'}),max_length=64)
    description = forms.CharField(label="description", widget=forms.Textarea(attrs={'placeholder':'Add Description'}),max_length=512)
    starting_bid = forms.FloatField(label="starting bid",widget=forms.Textarea(attrs={'placeholder':'20.0'}))
    image = forms.URLField(label="image URL",widget= forms.Textarea(attrs={'placeholder':'Image URL'}), required=False)
    category = forms.CharField(label="category", widget=forms.Textarea(attrs={'placeholder':'Category'}), required=False,max_length=64)
    
    def __init__(self, *args, **kwargs):
        super(NewAuctionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    

def index(request):
    return render(request, "auctions/index.html")


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
    
def create_auction(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("auctions:login"))
    if request.method == "POST":
        form = NewAuctionForm(request.POST)
        if form.is_valid():
            obj = AuctionListing()
            obj.title = form.cleaned_data['title']
            obj.description = form.cleaned_data['description']
            obj.starting_price = form.cleaned_data['starting_bid']
            obj.photo = form.cleaned_data['image']
            obj.is_active = True
            obj.category = Category.objects.get_or_create(name = form.cleaned_data['category'])[0]
            obj.owner = request.user
            obj.save()
            
            return HttpResponseRedirect(reverse("auctions:listing"))
        else:
            return render(
                request,
                "auctions/create.html",
                {"form": form},
            )
    else:
        return render(
            request,
            "auctions/create.html",
            {"form": NewAuctionForm()},
        )
 
def listing(request):
    return HttpResponse("HELLO")         
        
