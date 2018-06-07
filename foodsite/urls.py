from django.urls import path
from . import views
 
 
urlpatterns = [
	path('', views.home, name='home'),
	path('modalsubmit/', views.modalsubmit, name = 'modalsubmit'),
	path('helpform/', views.helpform, name = 'helpform')
]