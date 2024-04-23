from django.contrib import admin

# Register your models here.
from .models import SalesData2010,SalesData2011,SalesData2012

admin.site.register(SalesData2010)
admin.site.register(SalesData2011)
admin.site.register(SalesData2012)