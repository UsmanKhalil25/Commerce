from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.create,name = "create"),
    path("categories",views.categories,name = "categories"),
    path("displayCategory/<int:id>", views.displayCategory, name="displayCategory"),
    path("listing/<int:id>",views.listing,name = "listing"),
    path("addWatchlist/<int:id>",views.addWatchlist,name = "addWatchlist"),
    path("removeWatchlist/<int:id>",views.removeWatchlist,name = "removeWatchlist"),
    path("watchlist",views.watchlist,name = "watchlist"),
    path("addComment/<int:id>",views.addComment,name = "addComment"),
    path("placeBid/<int:id>",views.placeBid,name ="placeBid"),
    path("closeAuction/<int:id>",views.closeAuction,name = "closeAuction")
]

