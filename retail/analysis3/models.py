from django.db import models

class SalesData2010(models.Model):
    store = models.IntegerField()
    is_holiday = models.IntegerField()
    dept = models.IntegerField()
    weekly_sales = models.FloatField()
    year = models.IntegerField()
    month = models.IntegerField()
    week = models.IntegerField()

    class Meta:
        db_table = 'sales_data_2010'

class SalesData2011(models.Model):
    store = models.IntegerField()
    is_holiday = models.IntegerField()
    dept = models.IntegerField()
    weekly_sales = models.FloatField()
    year = models.IntegerField()
    month = models.IntegerField()
    week = models.IntegerField()

    class Meta:
        db_table = 'sales_data_2011'

class SalesData2012(models.Model):
    store = models.IntegerField()
    is_holiday = models.IntegerField()
    dept = models.IntegerField()
    weekly_sales = models.FloatField()
    year = models.IntegerField()
    month = models.IntegerField()
    week = models.IntegerField()

    class Meta:
        db_table = 'sales_data_2012'
