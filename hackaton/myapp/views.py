from django.shortcuts import render

def home(request):
    context = {
        'name' : 'Matteo Benassi',
        'car' : 'Renault Clio',
        'age' : 10,
    }
    return render(request, 'home.html', context)