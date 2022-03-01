from .views import(
	my_ads,delete_ad,approoved_ads,unapprooved_ads,update_ads
	)
from django.urls import path

app_name ="adds"

urlpatterns = [
	path('my_ads/',my_ads,name="my_ads"),
	path('update_ads/<post_id>/',update_ads,name="update_ads"),
	path('delete_ad/<post_id>/',delete_ad,name="delete_ad"),
	path('approoved_ads/',approoved_ads,name="approoved_ads"),
	path('unapprooved_ads/',unapprooved_ads,name="unapprooved_ads"),

]