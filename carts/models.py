import datetime

from django.db import models
from django.utils import timezone

class CartGroup(models.Model):
    group_name = models.CharField(max_length=30)
    group_color = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.group_name

    class Meta:
        ordering = ["group_name"]

class CartFleet(models.Model):
    name = models.CharField(max_length=30)
    date_acquired = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]

class Cart(models.Model):
    number = models.IntegerField()
    group = models.ManyToManyField(CartGroup)
    cart_fleet = models.ForeignKey(CartFleet, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number)

    class Meta:
        ordering = ["number"]

class DataCollection(models.Model):
    name = models.CharField(max_length=30, default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def __str__(self):
        return str(self.name)

class DataSet(models.Model):
    collection_date = models.DateField()
    amp_hours = models.FloatField()
    mileage = models.FloatField()
    hours = models.IntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    collection = models.ForeignKey(DataCollection, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.collection_date)

    class Meta:
        ordering = ["collection_date"]

class DataFile(models.Model):
    data_file = models.FileField(upload_to='uploads/')
    fleet = models.ForeignKey(CartFleet, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.data_file.name)

class Fault(models.Model):
     hour = models.IntegerField()
     code = models.IntegerField()
     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

     def __str__(self):
         return str(self.code)

     class Meta:
         ordering = ["hour"]




# Create your models here.
