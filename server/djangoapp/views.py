from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel, CarMake
from .restapis import get_dealers_from_cf, get_request, get_dealer_by_id, get_dealers_by_state, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        #username = request.POST['username']
        #password = request.POST['psw']
        username = request.POST.get('username')
        password = request.POST.get('psw')
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')

def static_template(request):
    # If the request method is GET
    if request.method == 'GET':
        return render(request, 'djangoapp/template.html')

def about_us(request):
    # If the request method is GET
    if request.method == 'GET':
        return render(request, 'djangoapp/about.html')

def contact_us(request):
    # If the request method is GET
    if request.method == 'GET':
        return render(request, 'djangoapp/contact.html')

# Create an `about` view to render a static about page
# def about(request):
# ...


# Create a `contact` view to return a static contact page
#def contact(request):

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships
#def get_dealerships(request):
#    context = {}
#    if request.method == "GET":
#        return render(request, 'djangoapp/index.html', context)
def get_dealerships(request):
    dealerState = "California"
    dealerId = 10
    context = dict()
    context = {"dealership_list": []}
    if request.method == "GET":
        url = "https://ideoalessand-3000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        for dealer in dealerships:
            context["dealership_list"].append({"id": dealer.id, "name": dealer.full_name, "city": dealer.city, "address": dealer.address,
            "zip": dealer.zip, "state" : dealer.st})
        # Return a list of dealer short name
        #print(context["dealership_list"])
        return render(request, 'djangoapp/index.html', context)
        #return HttpResponse(dealer_names)
        
def get_dealer_details(request, dealer_id):

    if request.method == "GET":
        url = "https://ideoalessand-5000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews"
        # Get dealers from the URL
        context = dict()
        context = {"reviews_list" : [], "dealer_id": dealer_id}
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        # Concat all dealer's short name
        #dealer_reviews = ' '.join([review.review for review in reviews])
        for review in reviews:
            #review.purchase_date = datetime.strptime(review.purchase_date, "%Y-%m-%d").strftime("%d-%m-%Y")
            sentiment = json.loads(review.sentiment)
            review.sentiment = 'neutral' if not sentiment["entities"] else sentiment["entities"][0]['sentiment']['label']
            #sentiment = json.loads(review.sentiment)
            #print(sentiment["entities"])
            context["reviews_list"].append({"review" : review})
        # Return a list of dealer short name
        return render(request, 'djangoapp/dealer_details.html', context)
        #return HttpResponse(dealer_reviews)
# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

def add_review(request, dealer_id):
    context = dict()
    cars = CarModel.objects.all()
    #print(cars)
    context = {"dealer_id" : dealer_id, "cars": cars}
    if request.method == 'GET':
        return render(request, 'djangoapp/add_review.html', context)
    elif request.user.is_authenticated and request.method == 'POST':
        # Get user information from request.POST
        #url0 = "https://ideoalessand-3000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        #dealer = get_dealer_by_id(url0, dealer_id)
        review = dict()
        review["time"] = datetime.utcnow().isoformat()
        review["dealership"] = dealer_id
        review["id"] = request.user.id
        review["name"] = request.user.username
        review["review"] = request.POST['review']
        review["purchase"] = request.POST['purchase']
        review["purchase_date"] = request.POST['purchase_date']
        mmy = request.POST['mmy']
        mmy = mmy.split("-")
        car_model = mmy[1]
        car_make = mmy[2]
        car_year = mmy[3]
        review["car_make"] = car_make
        review["car_model"] = car_model
        review["car_year"] = car_year
        json_payload = review
        url = "https://ideoalessand-5000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review"
        added_review = post_request(url, json_payload, dealer_id=dealer_id)
        print(added_review)
        return HttpResponse(added_review)
