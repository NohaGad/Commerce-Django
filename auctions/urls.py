from django.urls import path

from . import views

app_name = 'auctions'
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_auction, name="create"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category", views.category, name="category"),
    path("categorylisting/<str:category>", views.category_listing,name="category_listing"),
    path("bid/<int:id>",views.bidding, name="bidding"),
    path("comment/<int:id>",views.comment_view,name="comment"),
    path("close/<int:id>",views.close_auction,name="close")
]
