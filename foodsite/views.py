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
import json
import csv
sys.path.append('/home/ashish/Documents/github/foodweb/caffeclassifier/')
from foodclassify import main
# Create your views here.


def home(request):
	"""
	created for requests sent by dropzone. Takes a POST request
	as input argument and returns a JsonResponse containing the
	path to the image and the predictions.
	"""
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
	"""
	created for requests sent by modalform. Takes a POST request
	as input argument and returns a JsonResponse containing the
	path to the image and the predictions.
	"""
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
def appsubmit(request):
	"""
	created for requests sent by Food Diary App. Takes a POST request
	as input argument and returns a JSONResponse containing the predictions
	"""
	print('appsubmit request')
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		new_file = UploadFile(file = request.FILES['image'])
		new_file.save()
		img = 'foodsite/static/foodsite/' + new_file.file.name;
		l = ['foodclassify.py', img]
		probs = main(input_file=l)
		response = {'Result': 'Success'}
		response["Predictions"] = []
		for foodset in probs:
			response["Predictions"].append({"FoodName": foodset[0], "ver": 1})
		print(response)
		return JsonResponse(response)
	else:
		return JsonResponse({'Result': 'Upload not valid.'})

@csrf_exempt
def getinfo(request):
	"""
	created for requests sent by android application for getting
	the nutrition facts for a food item. Returns a json reponse
	containing the url of the food image, the nutrition facts and
	the version.
	"""
	print('getinfo request')
	if request.method == 'POST':
		print(request.POST)
		dishname = request.POST["dishname"]
		print(dishname)
		response = {}
		response['image_url'] = 'http://' + request.get_host() + '/static/foodsite/images/' + dishname.replace('_', '')+'.jpg';
		response['version'] = 1;
		f = open('nutrition.json')
		nutrition = json.load(f)
		f.close()
		jsonsearch = dishname + '_Nutrition'
		response['nutrition'] = nutrition[jsonsearch]
		print(nutrition[jsonsearch])
		response['ingredients'] = ['']
		response['Response'] = "Success"
		return JsonResponse(response)

		

@csrf_exempt
def helpform(request):
	"""
	created for taking input from the user in case the prediction
	of out model is wrong. takes a request containing the correct
	dish name specified by user and the imagename in the static
	files of this website.
	"""
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