from django.db import models

class Row(models.Model):
    row_name = models.CharField(max_length=30)

    def __str__(self):
        return self.row_name
    
    pass

class Cart(models.Model):
    number = models.FloatField()
    row = models.ForeignKey(Row, on_delete=models.CASCADE)
    amp_hours = models.FloatField()
    mileage = models.FloatField()
    hours = models.IntegerField()

    def __str__(self):
        return self.number

    class Meta:
        ordering = ["number"]
