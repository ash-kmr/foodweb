from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.urls import reverse
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import JsonResponse
from django import forms
from .models import UploadFile
from .forms import UploadFileForm
import sys
import csv
sys.path.append('/home/ashish/Documents/github/foodweb/caffeclassifier/')
from foodclassify import main
# Create your views here.

def home(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = UploadFile(file = request.FILES['file'])
            new_file.save()
            img = 'foodsite/static/foodsite/' + new_file.file.name;
            l = ['foodclassify.py', img]
            probs = main(input_file=l)
            print(probs)
            response = {}
            response['path'] = new_file.file.name
            for foodset in probs:
                if foodset[1] < 0.0001 : response[foodset[0]] = '0.0001'
                else : response[foodset[0]] = str(foodset[1])
            return JsonResponse(response)
    else:
        form = UploadFileForm()
    data = {'form': form}
    return render(request, 'foodsite/index.html', data)

@csrf_exempt
def modalsubmit(request):
    print('i just got called')
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = UploadFile(file = request.FILES['file'])
            new_file.save()
            img = 'foodsite/static/foodsite/' + new_file.file.name;
            l = ['foodclassify.py', img]
            probs = main(input_file=l)
            response = {}
            response['path'] = new_file.file.name
            for foodset in probs:
                if foodset[1] < 0.0001 : response[foodset[0]] = '0.0001'
                else : response[foodset[0]] = str(foodset[1])
            print('sending my response')
            return JsonResponse(response)
    else:
        return JsonResponse({'foo':'foo'})

@csrf_exempt
def helpform(request):
    print('igotcalled')
    if request.method == 'POST':
        imname = request.POST['imagename']
        dname = request.POST['dishname']
        towrite = [imname, dname]
        f = open('correction.csv', 'a')
        writer = csv.writer(f)
        writer.writerow(towrite)
        f.close()
        return JsonResponse({'success':'true'})
    else:
        return JsonResponse({'success':'false'})