from django.shortcuts import render
import json
from django.template import Template
# Create your views here.


def index(request):

    return render(request, 'frontend_app/index.html')
