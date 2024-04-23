from django.shortcuts import render
from django.contrib.auth.decorators import login_required
@login_required

def analysis5_view(request):
    return render(request, 'analysis5/analysis5.html')