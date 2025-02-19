from django.shortcuts import render

def home(request):
    context = {
        'name' : 'Hackaton',
        'age' : 10,
    }
    return render(request, 'home.html', context)

def prova(request):
    return render(request, 'prova.html')