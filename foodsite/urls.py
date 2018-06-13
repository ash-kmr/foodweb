from django.urls import path
from . import views
 
 
urlpatterns = [
	path('', views.home, name='home'),
	path('getinfo/', views.getinfo, name = 'getinfo'),
	path('modalsubmit/', views.modalsubmit, name = 'modalsubmit'),
	path('appsubmit/', views.appsubmit, name = 'appsubmit'),
	path('helpform/', views.helpform, name = 'helpform')
]
