from django.shortcuts import render

from django.http import HttpResponse

from django.template import loader, Context


# Create your views here.

def index(request):
    t = loader.get_template('index.html')
    c = Context({})
    # return HttpResponse('<h1>Hello Django</h1>')
    return HttpResponse(t.render(c))
