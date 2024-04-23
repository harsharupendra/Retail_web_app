from django.db import models

# Create your models here.

class SalesData(models.Model):
    store = models.IntegerField()
    temperature = models.FloatField()
    fuel_price = models.FloatField()
    cpi = models.FloatField()
    dept = models.IntegerField()
    weekly_sales = models.FloatField()
    year = models.IntegerField()
    month = models.IntegerField()
    week = models.IntegerField()

    def __str__(self):
        return f'Store {self.store}, Week {self.week} - Year {self.year}'
