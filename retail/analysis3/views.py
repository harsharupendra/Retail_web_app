import matplotlib.pyplot as plt
from io import BytesIO
import pandas as pd
import base64
from django.shortcuts import render
from .models import SalesData2010, SalesData2011, SalesData2012
from django.contrib.auth.decorators import login_required

# Mapping years to models
model_mapping = {
    '2010': SalesData2010,
    '2011': SalesData2011,
    '2012': SalesData2012,
}

@login_required
def analysis3_view(request):
    year = request.GET.get('year', '2010')
    store = int(request.GET.get('store', '1'))
    dept = int(request.GET.get('dept', '1'))

    
    DataModel = model_mapping[year]
    
    # Fetch data from the selected model
    data = DataModel.objects.all().values('store', 'dept', 'weekly_sales', 'week', 'is_holiday')
    df = pd.DataFrame(list(data))
    holiday_weeks = df[df['is_holiday'] == 0]['week'].unique()

    if df[(df['store'] == store) & (df['dept'] == dept)].empty:
        
        message = "No data available for the selected store and department combination."
        return render(request, 'analysis3/analysis3.html', {
            'message': message,
            'stores': range(1, 46),
            'departments': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 40, 41, 42, 44, 46, 48, 49, 52, 54, 55, 56, 58, 59, 60, 67, 71, 72, 74, 79, 80, 81, 82, 83, 85, 87, 90, 91, 92, 93, 94, 95, 96, 97, 98, 45, 51, 99, 77, 47, 78, 39, 50, 43, 65],
            'years': range(2010, 2013)
        })

    
    filtered_data = df[(df['store'] == store)]
    weekly_avg_sales = filtered_data.groupby('week')['weekly_sales'].mean()
    
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    weekly_avg_sales.plot(ax=ax1, marker='o', linestyle='-')
    for week in holiday_weeks:
        ax1.scatter(week, weekly_avg_sales[week], color='red', zorder=5)
    ax1.set_title(f'Average Weekly Sales for Store {store} in {year}')
    ax1.set_xlabel('Week')
    ax1.set_ylabel('Average Sales')
    ax1.grid(True)
    buf1 = BytesIO()
    plt.savefig(buf1, format='png')
    plt.close(fig1)
    plot1 = base64.b64encode(buf1.getvalue()).decode('utf-8')
    buf1.close()

    
    filtered_data2 = df[(df['dept'] == dept)]
    weekly_avg_sales2 = filtered_data2.groupby('week')['weekly_sales'].mean()
    
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    weekly_avg_sales2.plot(ax=ax2, marker='o', linestyle='-')
    for week in holiday_weeks:
        ax2.scatter(week, weekly_avg_sales2[week], color='red', zorder=5)
    ax2.set_title(f'Average Weekly Sales for Department {dept} in {year}')
    ax2.set_xlabel('Week')
    ax2.set_ylabel('Average Sales')
    ax2.grid(True)
    buf2 = BytesIO()
    plt.savefig(buf2, format='png')
    plt.close(fig2)
    plot2 = base64.b64encode(buf2.getvalue()).decode('utf-8')
    buf2.close()

    
    filtered_data3 = df[(df['dept'] == dept) & (df['store'] == store)]
    weekly_avg_sales3 = filtered_data3.groupby('week')['weekly_sales'].mean()
    
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    weekly_avg_sales3.plot(ax=ax3, marker='o', linestyle='-')
    for week in holiday_weeks:
        ax3.scatter(week, weekly_avg_sales3[week], color='red', zorder=5)
    ax3.set_title(f'Average Weekly Sales for Department {dept} at Store {store} in {year}')
    ax3.set_xlabel('Week')
    ax3.set_ylabel('Average Sales')
    ax3.grid(True)
    buf3 = BytesIO()
    plt.savefig(buf3, format='png')
    plt.close(fig3)
    plot3 = base64.b64encode(buf3.getvalue()).decode('utf-8')
    buf3.close()

    return render(request, 'analysis3/analysis3.html', {
        'plot1': plot1,
        'plot2': plot2,
        'plot3': plot3,
        'stores': range(1, 46),
        'departments': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 40, 41, 42, 44, 46, 48, 49, 52, 54, 55, 56, 58, 59, 60, 67, 71, 72, 74, 79, 80, 81, 82, 83, 85, 87, 90, 91, 92, 93, 94, 95, 96, 97, 98, 45, 51, 99, 77, 47, 78, 39, 50, 43, 65],
        'years': range(2010, 2013)
    })
