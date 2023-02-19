from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from . import extractor

def welcome(request):
    return HttpResponse('Welcome to our API')

@csrf_exempt
def extract(request):
    print("Doint the work")
    if request.method=='POST':
        print(type(json.loads(request.body)["text"]))
        data = json.loads(request.body)["text"]
        summary = { "data": extractor.extractor(data) }
        print(json.dumps(summary))
        return HttpResponse(json.dumps(summary))
    return HttpResponse("Invalid Request")