from django.shortcuts import render
from django.http import HttpResponse
from .helpers import content

def index(request): #new
    default_context = content.default_context()
    context = {
        'default_context': default_context
    }
    return render(template_name='home.html',request=request, context=context)