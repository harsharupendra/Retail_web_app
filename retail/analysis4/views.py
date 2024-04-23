from django.shortcuts import render
from django.contrib.auth.decorators import login_required
@login_required
def analysis4_view(request):
    return render(request, 'analysis4/analysis4.html')