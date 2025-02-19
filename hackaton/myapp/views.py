from django.shortcuts import render

def home(request):
    return render(request, 'home.html', {'title': 'Home Page'})

def about(request):
    return render(request, 'about.html', {'title': 'About Page'})