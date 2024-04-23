from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Username already exists')
            else:
                user = form.save()
                login(request, user)
                return redirect('dashboard')  
    else:
        form = SignUpForm()
    return render(request, 'accounts/register.html', {'form': form})
