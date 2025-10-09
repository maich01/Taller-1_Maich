from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def home(request):
    #return HttpResponse ('<h1>Welcome to home page</h1>')
    #return render(request, 'home.html')
    return render(request, 'home.html', {'name':'Mariana Jaramillo Herrera'})




def about(request):
    #return HttpResponse ('<h1>Welcome to about page</h1>')
    return render(request, 'about.html', {'name':'Mariana Jaramillo Herrera'})
