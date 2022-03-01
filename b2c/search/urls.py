from .views import search
from django.urls import path


app_name ="search"


urlpatterns = [
	path('search/',search,name="search"),
]
