from rest_auth.views import(
	Register,activate,LoginView,
	user_profile,update_password,
	verify_token,user_password_reset,
    veryfy_otp,
	)
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

app_name="rest_auth"
urlpatterns = [
    path('register/',Register.as_view(),name="register"),
    path('activate/<data>',activate,name="activate"),
    path('login/',LoginView.as_view(),name="login"),
    path('user_profile/',user_profile,name="user_profile"),
    path('update_password/',update_password,name="update_password"),
    path('verify_token/',verify_token,name="verify_token"),
    path('user_password_reset/',user_password_reset,name="user_password_reset"),
    path('veryfy_otp/',veryfy_otp,name="veryfy_otp"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
