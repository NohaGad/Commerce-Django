from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from django.shortcuts import get_object_or_404


from .models import User, AuctionListing, Category, Bid

DEFAULT_IMAGE ='data:image/svg+xml;charset=UTF-8,<svg%20width%3D"286"%20height%3D"180"%20xmlns%3D"http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg"%20viewBox%3D"0%200%20286%20180"%20preserveAspectRatio%3D"none"><defs><style%20type%3D"text%2Fcss">%23holder_18aa591097b%20text%20%7B%20fill%3Argba(255%2C255%2C255%2C.75)%3Bfont-weight%3Anormal%3Bfont-family%3AHelvetica%2C%20monospace%3Bfont-size%3A14pt%20%7D%20<%2Fstyle><%2Fdefs><g%20id%3D"holder_18aa591097b"><rect%20width%3D"286"%20height%3D"180"%20fill%3D"%23777"><%2Frect><g><text%20x%3D"107.1937484741211"%20y%3D"96.24000034332275">286x180<%2Ftext><%2Fg><%2Fg><%2Fsvg>'


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
    
class BiddingForm(ModelForm):
    class Meta:
        model = Bid
        fields = [ "price"]
        
def index(request):
    active_auctions = AuctionListing.objects.filter(is_active = True)
    return render(request, "auctions/index.html", {"active_auctions":active_auctions , "default_image":DEFAULT_IMAGE})


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
            obj.category = Category.objects.get_or_create(name = form.cleaned_data['category'])[0] if form.cleaned_data['category'] else None
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
 
def listing(request, id):
    auction_listing = get_object_or_404(AuctionListing , id=id)
    bidding_form = BiddingForm()
    return render(request, "auctions/listingpage.html",{"auction_listing" : auction_listing , "default_image": DEFAULT_IMAGE, "bidding_form": bidding_form}) 
    
def bidding(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("auctions:login"))
    auction_listing = get_object_or_404(AuctionListing , id=id)
    if request.method == "POST":
        bid = Bid()
        bid.bidder = request.user
        bid.auction = auction_listing
        form = BiddingForm(request.POST,instance=bid)
        if form.is_valid():
            bid.price = form.cleaned_data["price"]
            bid.save()
            return HttpResponseRedirect(reverse("auctions:listing",args=(id,)))
        else:
            return render(request, "auctions/listingpage.html",{"auction_listing" : auction_listing , "default_image": DEFAULT_IMAGE, "bidding_form": form}) 

    else:
        return HttpResponseRedirect(reverse("auctions:listing",args=(id,)))
            
        
def category(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("auctions:login"))
    categories = Category.objects.all()
    return render(request, "auctions/category.html" ,{"categories":categories})
    
def category_listing(request,category):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("auctions:login"))
    query_set= Category.objects.filter(name=category)
    category_obj = get_object_or_404(query_set)
    active_auctions = category_obj.auctionlisting_set.all()
    return render(request, "auctions/category_list.html", {"active_auctions":active_auctions , "default_image":DEFAULT_IMAGE,"category":category_obj})
 
    
def watchlist(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("auctions:login"))  
    active_auctions = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {"active_auctions":active_auctions , "default_image":DEFAULT_IMAGE})
 
        
        
