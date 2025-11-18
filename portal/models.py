from django.db import models

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name="models")
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    type = models.CharField(max_length=50, blank=True)  # e.g. SUV, Sedan, Coupe

    def __str__(self):
        return f"{self.year} {self.make.name} {self.name}"
