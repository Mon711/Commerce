from django.urls import path

from . import views

urlpatterns = [
    path("", views.active_listings, name="listings"),
    path("homepage", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.create,name="create"),
    path("listings/item/<int:item_id>",views.item,name="item"),
    path("listings/item/<int:item_id>/bid",views.item,name="bid"),
    path("listings/item/<int:item_id>/bid/close",views.close_bid,name="close"),
    path("listings/item/<int:item_id>/comment",views.enter_comment,name="comment"),
    path("listing/item/<int:item_id>/watchlist",views.wathclist_item,name="watchlist"),
    path("listing/item/<int:item_id>/watchlist/removed",views.rem_wathclist,name="remove"),
    path("listings/watchlisted_items",views.view_watchlist,name="watchlisted"),
    path("listings/categories",views.view_categories,name="category")
]
