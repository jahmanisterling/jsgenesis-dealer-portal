import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

API = "http://localhost:3000"   # Express backend


# -----------------------------
# HOME — Show all dealers
# -----------------------------
def home(request):
    raw_dealers = requests.get(f"{API}/dealers").json()

    dealers = []
    for d in raw_dealers:
        d["id"] = d["_id"]       # Convert Mongo _id → id
        dealers.append(d)

    return render(request, "portal/home.html", {"dealers": dealers})


# -----------------------------
# DEALER DETAILS — reviews for 1 dealer
# -----------------------------
def dealer_details(request, dealer_id):
    reviews = requests.get(f"{API}/reviews/dealer/{dealer_id}").json()
    return render(request, "portal/dealer_details.html", {
        "reviews": reviews,
        "dealer_id": dealer_id
    })


# -----------------------------
# ADD REVIEW — user must be logged in
# -----------------------------
@login_required
def add_review(request, dealer_id):
    if request.method == "POST":
        reviewer = request.user.username
        rating = request.POST.get("rating")
        text = request.POST.get("review")

        payload = {
            "dealerId": dealer_id,
            "reviewer": reviewer,
            "rating": int(rating),
            "review": text,
            "sentiment": "neutral"   # sentiment analyzer handles real one
        }

        requests.post(f"{API}/reviews", json=payload)
        return redirect("dealer_details", dealer_id=dealer_id)

    return render(request, "portal/add_review.html", {"dealer_id": dealer_id})


def filter_by_state(request):
    # Get state value from ?state=...
    state = request.GET.get("state", "").strip()

    # If no state entered, just show all dealers
    if not state:
        return redirect("home")

    # Normalize capitalization, e.g. "kansas" -> "Kansas"
    state_param = state.title()

    # Call Express backend
    raw = requests.get(f"{API}/dealers/state/{state_param}").json()

    dealers = []
    for d in raw:
        d["id"] = d["_id"]
        dealers.append(d)

    return render(request, "portal/home.html", {
        "dealers": dealers,
        "filtered_state": state_param
    })

# -----------------------------
# SENTIMENT ANALYZER
# -----------------------------
def analyze_sentiment(request):
    text = request.GET.get("text", "")

    if not text:
        return JsonResponse({"error": "No text provided"})

    text_lower = text.lower()

    if "good" in text_lower or "love" in text_lower or "great" in text_lower:
        sentiment = "positive"
    elif "bad" in text_lower or "hate" in text_lower:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return JsonResponse({"text": text, "sentiment": sentiment})



# ===============================================================
# AUTHENTICATION — LOGIN, SIGNUP, LOGOUT
# ===============================================================
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


# -----------------------------
# LOGIN
# -----------------------------
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "portal/login.html", {
                "error": "Invalid credentials"
            })

    return render(request, "portal/login.html")


# -----------------------------
# SIGN UP
# -----------------------------
def signup_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            return render(request, "portal/signup.html", {
                "error": "Passwords do not match"
            })

        user = User.objects.create_user(username=username, password=password1)
        login(request, user)
        return redirect("home")

    return render(request, "portal/signup.html")


# -----------------------------
# LOG OUT
# -----------------------------
def logout_user(request):
    logout(request)
    return redirect("home")
