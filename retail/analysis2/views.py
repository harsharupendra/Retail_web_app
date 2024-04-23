
from django.shortcuts import render
from analysis1.models import SalesData
from django.db.models import Avg,Sum

from io import BytesIO
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.contrib.auth.decorators import login_required

def generate_plot(year_to_filter, month_to_filter):
    
    filtered_data = SalesData.objects.filter(year=year_to_filter, month=month_to_filter).values('store', 'temperature', 'fuel_price', 'cpi')

    fig, axes = plt.subplots(4, 1, figsize=(10, 15))
    average_monthly_sales = filtered_data.annotate(avg_monthly_sales=Avg('weekly_sales')).values('store', 'avg_monthly_sales')

    
    filtered_data = list(filtered_data)

    
    
    axes[0].plot([data['store'] for data in average_monthly_sales], [data['avg_monthly_sales'] for data in average_monthly_sales], marker='o', linestyle='-', color='y')
    axes[0].set_title('Average Monthly Sales by Store')
    axes[0].set_xlabel('Store')
    axes[0].set_ylabel('Average Monthly Sales')

    
    axes[1].plot([data['store'] for data in filtered_data], [data['fuel_price'] for data in filtered_data], marker='o', linestyle='-', color='b')
    axes[1].set_title('Fuel Price by Store')
    axes[1].set_xlabel('Store')
    axes[1].set_ylabel('Fuel Price')

    
    axes[2].plot([data['store'] for data in filtered_data], [data['temperature'] for data in filtered_data], marker='o', linestyle='-', color='r')
    axes[2].set_title('Temperature by Store')
    axes[2].set_xlabel('Store')
    axes[2].set_ylabel('Temperature')

    
    axes[3].plot([data['store'] for data in filtered_data], [data['cpi'] for data in filtered_data], marker='o', linestyle='-', color='g')
    axes[3].set_title('CPI by Store')
    axes[3].set_xlabel('Store')
    axes[3].set_ylabel('CPI')

    
    buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    
    plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    return plot_data

def get_top_10_entries(year_to_filter, month_to_filter):
    
    top_10_data = SalesData.objects.filter(
        year=year_to_filter, month=month_to_filter
    ).values(
        'store', 'dept', 'fuel_price', 'temperature', 'cpi'  
    ).annotate(
        avg_monthly_sales=Avg('weekly_sales')  
    ).order_by(
        '-avg_monthly_sales' 
    )[:10]  

    return top_10_data

@login_required
def analysis_view(request):
   
    default_year = 2010
    default_month = 1

    
    if request.method == 'POST':
        year = request.POST.get('year', default_year)
        month = request.POST.get('month', default_month)
    else:
        year = default_year
        month = default_month

    
    try:
        year = int(year)
        month = int(month)
    except ValueError:
        
        year = default_year
        month = default_month

   
    

    
    top_10_data = get_top_10_entries(year, month)
    for entry in top_10_data:
        entry['cpi'] = round(entry['cpi'], 2)
        entry['avg_monthly_sales'] = round(entry['avg_monthly_sales'], 2)
    

    plot_data = generate_plot(year, month)
    
    data = SalesData.objects.filter(year=year, month=month)
    avg_fuel_price = data.aggregate(avg_fuel_price=Avg('fuel_price'))['avg_fuel_price']
    avg_temperature = data.aggregate(avg_temperature=Avg('temperature'))['avg_temperature']
    avg_cpi = data.aggregate(avg_cpi=Avg('cpi'))['avg_cpi']
    gross_monthly_sales = data.aggregate(gross_monthly_sales=Sum('weekly_sales'))['gross_monthly_sales']

    
    fuel_price_unit = "USD per gallon" 
    monthly_sales_unit = "USD (x10k)"  
    temperature_unit = "°F"  
    cpi_unit = "index"  

   
    return render(request, 'analysis2/analysis2.html', {
        'data': top_10_data,
        'gross_monthly_sales': gross_monthly_sales,
        'avg_fuel_price': avg_fuel_price,
        'avg_temperature': avg_temperature,
        'avg_cpi': avg_cpi,
        'monthly_sales_unit': monthly_sales_unit,
        'fuel_price_unit': fuel_price_unit,
        'temperature_unit': temperature_unit,
        'cpi_unit': cpi_unit,
        'default_year': default_year,
        'default_month': default_month,
        'plot_data': plot_data
    })
