from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max

from .models import User, Listing, Bid, Comment


def index(request):
    return render(request, "auctions/index.html")


def active_listings(request):
    return render(
        request, "auctions/listings.html", {"listings": Listing.objects.all()}
    )


@login_required(login_url="login")
def item(request, item_id):
    listing = Listing.objects.get(pk=item_id)
    x = Bid.objects.filter(item_id=item_id).aggregate(Max("bid"))
    max_bid = x["bid__max"]

    comments = Comment.objects.filter(itemID=listing)

    if comments.exists():
        comments = comments
    else:
        comments = "N/A"

    user_in_session = request.session["username"]
    username = User.objects.get(username=user_in_session)

    if username.watchlist.filter(id=item_id).exists():
        watchlisted = True
    else:
        watchlisted = False

    if request.method == "GET":
        if max_bid != None:
            y = Bid.objects.get(bid=max_bid)
            max_bidder = str(y.uname)
        else:
            max_bidder = None

        color = None
        message = None

        # # return HttpResponse(max_bidder)
        # if 'username' not in request.session:
        #     request.session['username'] = None

    else:
        bid = request.POST
        amt = float(bid["amount"])

        if max_bid is not None and amt <= max_bid:
            message = "Your amount is less than or equal to the highest bid."
            color = "danger"
            y = Bid.objects.get(bid=max_bid)
            max_bidder = str(y.uname)
        else:
            message = "You bid has been successfully placed!!"
            color = "success"
            bid = Bid(item_id=listing.id, bid=amt, uname=username)
            max_bidder = str(username)
            max_bid = amt
            bid.save()

    # return HttpResponse(listing.status)
    return render(
        request,
        "auctions/item.html",
        {
            "item": listing,
            "owner": str(listing.owner),
            "logged_in_user": str(request.session["username"]),
            "item_id": item_id,
            "message": message,
            "color": color,
            "maxBid": max_bid,
            "maxBidder": max_bidder,
            "comments": comments,
            "watchlisted": watchlisted,
        },
    )


@login_required(login_url="login")
def close_bid(request, item_id):
    item = Listing.objects.get(pk=item_id)
    item.status = "Closed"

    bidding = Bid.objects.filter(item_id=item_id).aggregate(Max("bid"))
    maxBid = bidding["bid__max"]

    x = Bid.objects.get(bid=maxBid)
    maxBidder = str(x.uname)

    item.save()

    return render(request, "auctions/closed.html", {"bid": maxBid, "bidder": maxBidder})


@login_required(login_url="login")
def enter_comment(request, item_id):
    text = request.POST["commentText"]
    user_in_session = request.session["username"]
    username = User.objects.get(username=user_in_session)
    item_id = Listing.objects.get(pk=item_id)

    # return HttpResponse(item)
    commentByUser = Comment(username=username, itemID=item_id, text=text)
    commentByUser.save()

    return HttpResponseRedirect(reverse("item", args=[item_id]))


@login_required(login_url="login")
def wathclist_item(request, item_id):
    user_in_session = request.session["username"]
    user = User.objects.get(username=user_in_session)
    item = Listing.objects.get(pk=item_id)

    user.watchlist.add(item)

    return HttpResponseRedirect(reverse("item", args=[item_id]))


@login_required(login_url="login")
def rem_wathclist(request, item_id):
    user_in_session = request.session["username"]

    user = User.objects.get(username=user_in_session)
    item = Listing.objects.get(pk=item_id)
    user.watchlist.remove(item)

    return HttpResponseRedirect(reverse("item", args=[item_id]))


@login_required(login_url="login")
def view_watchlist(request):
    user_in_session = request.session["username"]

    user = User.objects.get(username=user_in_session)

    items = user.watchlist.all()

    if not items.exists():
        items = None

    return render(request, "auctions/watchlist.html", {"items": items})


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            request.session["username"] = username
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))

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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)

        request.session["username"] = username
        return HttpResponseRedirect(reverse("index"))
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        return render(request, "auctions/register.html")


@login_required(login_url="login")
def create(request):
    if request.method == "POST":
        listing = request.POST
        title = listing["title"]
        desc = listing["description"]
        startingBid = listing["startBid"]

        user_in_session = request.session["username"]

        user_object = User.objects.get(username=user_in_session)
        # user_name = user_object.username

        if listing["imgUrl"] is not "":
            url = listing["imgUrl"]
        else:
            url = "N/A"

        x = Listing(
            title=title,
            description=desc,
            start_bid=startingBid,
            url_pic=url,
            owner=user_object,
        )
        x.save()

        return HttpResponseRedirect(reverse("listings"))
    else:
        return render(request, "auctions/create.html")


def view_categories(request):
    items = Listing.objects.all()
    titles = []

    for item in items:
        titles.append(item.title)

    Electronics = []
    Sports = []
    Apparel = []
    Home = []
    Other = []

    categories = []

    for title in titles:
        added_to_list = False

        for word in ["earphones", "phone", "watch"]:
            if word in title.lower():
                item_id = Listing.objects.get(title=title).id
                item = {title: item_id}
                Electronics.append(item)
                added_to_list = True
                break

        if added_to_list:
            continue

        for word in ["bat", "ball", "shoes", "bands", "weights"]:
            if word in title.lower():
                item_id = Listing.objects.get(title=title).id
                item = {title: item_id}
                Sports.append(item)
                added_to_list = True
                break

        if added_to_list:
            continue

        for word in ["shirt", "jeans", "jacket", "bags", "handbags", "dress", "jersey"]:
            if word in title.lower():
                item_id = Listing.objects.get(title=title).id
                item = {title: item_id}
                Apparel.append(item)
                added_to_list = True
                break

        if added_to_list:
            continue

        for word in ["microwave", "utensils", "fridge", "refrigerator", "furniture"]:
            if word in title.lower():
                item_id = Listing.objects.get(title=title).id
                item = {title: item_id}
                Home.append(item)
                added_to_list = True
                break

        if not added_to_list:
            item_id = Listing.objects.get(title=title).id
            item = {title: item_id}
            Other.append(item)

    categories = {
        "Electronics": Electronics,
        "Sports": Sports,
        "Apparel": Apparel,
        "Home": Home,
        "Other": Other,
    }

    return render(request, "auctions/categories.html", {"categories": categories})
