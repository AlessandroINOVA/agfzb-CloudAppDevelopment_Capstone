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
# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
