from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required


@login_required
def dashboard_view(request):
    context = {}
    return render(request, 'dashboard/dashboard.html', context)
