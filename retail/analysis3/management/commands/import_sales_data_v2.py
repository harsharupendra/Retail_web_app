import csv
from django.core.management.base import BaseCommand
from analysis3.models import SalesData2010, SalesData2011, SalesData2012  

class Command(BaseCommand):
    help = 'Imports sales data into the database'

    def handle(self, *args, **kwargs):
        csv_files = [
            {'model': SalesData2010, 'file_path': 'analysis3/data/file_2010.csv'},
            {'model': SalesData2011, 'file_path': 'analysis3/data/file_2011.csv'},
            {'model': SalesData2012, 'file_path': 'analysis3/data/file_2012.csv'}
        ]

        for csv_file in csv_files:
            model = csv_file['model']
            file_path = csv_file['file_path']

            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip the header row
                for row in reader:
                    model.objects.create(
                        store=int(row[1]),
                        is_holiday=int(row[2]),
                        dept=int(row[3]),
                        weekly_sales=float(row[4]),
                        year=int(row[5]),
                        month=int(row[6]),
                        week=int(row[7])
                    )

            self.stdout.write(self.style.SUCCESS(f'Data imported successfully for {model.__name__}!'))
