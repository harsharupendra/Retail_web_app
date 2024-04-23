import csv
from django.core.management.base import BaseCommand
from analysis1.models import SalesData

class Command(BaseCommand):
    help = 'Imports sales data into the database'

    def handle(self, *args, **kwargs):
        csv_file_path = 'analysis1/data/re.csv'

        with open(csv_file_path, 'r') as f:
            reader = csv.reader(f)
            next(reader) 
            for row in reader:
                
                dept = int(float(row[5]))  
               
                SalesData.objects.create(
                    store=int(row[1]),
                    temperature=float(row[2]),
                    fuel_price=float(row[3]),
                    cpi=float(row[4]),
                    dept=dept,
                    weekly_sales=float(row[6]),
                    year=int(row[7]),
                    month=int(row[8]),
                    week=int(row[9])
                )

        self.stdout.write(self.style.SUCCESS('Sales data imported successfully!'))
