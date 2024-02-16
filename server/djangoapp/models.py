from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarModel(models.Model):
    dealer_id = models.IntegerField(null=True)
    name = models.CharField(max_length=200)
    typ = models.CharField(max_length=200)
    year = models.DateField(null=True)
    
    # Create a toString method for object string representation
    def __str__(self):
        return "Dealer id: " + str(self.dealer_id) + "," + \
            "Name: " + self.name + ", Type: " + self.typ + ", Year: " + str(self.year)

class CarMake(models.Model):
    name = models.CharField(null=True, max_length=100)
    description = models.CharField(max_length=500)
    model = models.ForeignKey(CarModel, null=True, on_delete=models.CASCADE)
    
    # Create a toString method for object string representation
    def __str__(self):
        return "Name: " + self.name + "," + \
            "Description: " + self.description

class DealerReview(models.Model):
    dealership = models.CharField(null=True, max_length=100)
    name = models.CharField(null=True, max_length=50)
    purchase = models.CharField(null=True, max_length=50)
    review = models.CharField(null=True, max_length=100)
    purchase_date = models.DateField(null=True, max_length=50)
    car_make = models.CharField(null=True, max_length=50)
    car_model = models.CharField(null=True, max_length=100)
    car_year = models.DateField(null=True, max_length=50)
    sentiment = models.CharField(null=True, max_length=50)
    review_id = models.IntegerField(null=False)
    
    # Create a toString method for object string representation
    def __str__(self):
        return "dealership: " + str(self.dealership) + \
            ", name: " + str(self.name) + ", purchase: " + str(self.purchase) + \
            ", review: " + str(self.review) + ", purchase_date: " + str(self.purchase_date) + \
            ", car_make: " + str(self.car_make) + ", car_model: " + str(self.car_model) + \
            ", car_year: " + str(self.car_year) + ", sentiment: " + str(self.sentiment) + \
            ", review_id: " + str(self.review_id) 
# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
