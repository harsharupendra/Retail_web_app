from django.shortcuts import render
from .models import SalesData
from django.db.models import Avg

from io import BytesIO
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from django.contrib.auth.decorators import login_required




def generate_plot(year_to_filter, week_to_filter):
    
    filtered_data = SalesData.objects.filter(year=year_to_filter, week=week_to_filter).values('store', 'temperature', 'fuel_price', 'cpi')

    fig, axes = plt.subplots(4, 1, figsize=(10, 15))
    average_weekly_sales = filtered_data.annotate(avg_weekly_sales=Avg('weekly_sales')).values('store', 'avg_weekly_sales')

    
    filtered_data = list(filtered_data)

    
    
    axes[0].plot([data['store'] for data in average_weekly_sales], [data['avg_weekly_sales'] for data in average_weekly_sales], marker='o', linestyle='-', color='y')
    axes[0].set_title('Average Weekly Sales by Store')
    axes[0].set_xlabel('Store')
    axes[0].set_ylabel('Average Weekly Sales')

    
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
    
    # Encode the plot to base64
    plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    return plot_data

@login_required
def analysis_view(request):
    
    default_year = 2010
    default_week = 1

    
    if request.method == 'POST':
        year = request.POST.get('year', default_year)
        week = request.POST.get('week', default_week)
    else:
        year = default_year
        week = default_week
    
    try:
        week = int(week)
    except ValueError:
        week = default_week
    
    data = SalesData.objects.filter(year=year, week=week)

    
    sorted_data = data.order_by('-weekly_sales')

   
    top_10_data = sorted_data.values('store','dept','fuel_price', 'temperature','cpi','weekly_sales')[:10]
    for entry in top_10_data:
        entry['cpi'] = round(entry['cpi'], 2)
        entry['weekly_sales'] = round(entry['weekly_sales'], 2)

    
    avg_fuel_price = data.aggregate(avg_fuel_price=Avg('fuel_price'))['avg_fuel_price']
    avg_weekly_sales = data.aggregate(avg_weekly_sales=Avg('weekly_sales'))['avg_weekly_sales'] 
    avg_temperature = data.aggregate(avg_temperature=Avg('temperature'))['avg_temperature']
    avg_cpi = data.aggregate(avg_cpi=Avg('cpi'))['avg_cpi']

    plot_data = generate_plot(year, week)

    
    fuel_price_unit = "USD per gallon"  
    weekly_sales_unit = "USD (x10k)"  
    temperature_unit = "°F"  
    cpi_unit = "index"  

    
    return render(request, 'analysis1/analysis1.html', {
        'data': top_10_data,
        'avg_fuel_price': avg_fuel_price,
        'avg_weekly_sales': avg_weekly_sales,
        'avg_temperature': avg_temperature,
        'avg_cpi': avg_cpi,
        'fuel_price_unit': fuel_price_unit,
        'weekly_sales_unit': weekly_sales_unit,
        'temperature_unit': temperature_unit,
        'cpi_unit': cpi_unit,
        'default_year': default_year,
        'default_week': default_week,
        'plot_data': plot_data
    })
