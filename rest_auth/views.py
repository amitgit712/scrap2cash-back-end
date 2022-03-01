from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response	
from rest_auth.models import User,UserProfile,PasswordChanged
from rest_auth.serializers import RegisterSerializer
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.contrib.auth import authenticate,login 
import jwt
from rest_framework_jwt.serializers import jwt_payload_handler
from viit import settings
from django.contrib.auth.signals import user_logged_in
import json 
from rest_auth.jwt_middle_ware import JWTAuthentication
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
#import base64 
from admin_dashboard.models import(
	BussinessType,Category,
	Subcategory,ProductType
	)
import random
from rest_framework.decorators import api_view, renderer_classes


class Register(APIView):
	def get(self,request, format=None): 
		user = User.objects.all()
		serializer = RegisterSerializer(user, many=True)
		return Response(serializer.data)
	def post(self, request, format=None):
		inactive_email = self.request.data['email']
		#print("*/**/*/*email",inactive_email)
		try:
			inactive_user = User.objects.get(email=inactive_email,verify_email=False)
			inactive_user.delete()
			#print("/*/*/*//*/*/* inactive",inactive_user.delete())
		except:
			pass
		serializer = RegisterSerializer(data=request.data)
		if serializer.is_valid():
			if ('password' in self.request.data): 
				password = make_password(self.request.data['password'])
				instance = serializer.save(password=password)		
				message = "Click on the below url to activate your account"+  "\n \n"+ str(settings.BACKEND_URL)+"/activate/"+str(jwt.encode({"id":instance.id},settings.JWT_SECRET_KEY)).split("b'")[1].split("'")[0]#str(instance.id)
				msg = EmailMessage('Acitvate Your Account', message, to=[self.request.data['email']], from_email=settings.DEFAULT_FROM_EMAIL)
				msg.send()
				serializer.save()
				return Response({"response":serializer.data['email']}, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def activate(request,data):
	# print("*/*/*/*/*/*/*/*/*",data.split("b'")[1].split("'")[0])
	ids = jwt.decode(data,settings.JWT_SECRET_KEY,algorithms=['HS256'])
	print("*/*/*/*/*/*/*",ids)
	activate_user = User.objects.get(id=ids['id'])
	activate_user.verify_email = True
	activate_user.is_active = True
	activate_user.save()	
	return HttpResponseRedirect(str(settings.FRONTEND_URL)+"/login")


class LoginView(APIView):
	def post(self,request):
		# try:
		email = json.loads(request.body.decode("utf-8"))['email']
		password =  json.loads(request.body.decode("utf-8"))['password']
		auth = authenticate(self.request,username=email,password=password)
		#print("/**/*/*/*/*/ auth",auth)
		if auth is not None:
			try:
				check_user = User.objects.filter(email=email,verify_email=True,is_active=True)
				#print("/*/*/*/ checked user",check_user)
				if check_user:
					for i in check_user:
						payload = jwt_payload_handler(i)
						token = jwt.encode(payload, settings.JWT_SECRET_KEY)
						user_details = {}
						user_details['first_name'] = "%s" % (i.first_name)
						user_details['last_name'] = "%s" % (i.last_name)
						user_details['email'] = "%s" % (i.email)
						user_details['token'] = token
						user_logged_in.send(sender=i.__class__,request=request, user=i)
						return Response(user_details, status=status.HTTP_200_OK)
				else:
					res = {
					'error': 'You are account is not active check your email and follow the link'
					}
					return JsonResponse(res,safe=False)

			except Exception as e:
				return JsonResponse({'error':'Your account is not activated kindly check your mail'},safe=False)
		else:
			res = {
			'error': 'Invalid credentials'}
			return JsonResponse(res,safe=False)# status=status.HTTP_403_FORBIDDEN)
		# except KeyError:
		# 	res = {'error': 'please provide a email and a password'}
		# 	return Response(res)

########### Location ##############
# from geopy.geocoders import Nominatim
# geolocator = Nominatim(user_agent="geoapiExercises")
# def city_state_country(coord):
#     location = geolocator.reverse(coord, exactly_one=True)
#     address = location.raw['address']
#     city = address.get('city', '')
#     state = address.get('state', '')
#     country = address.get('country', '')
#     return city, state, country
# print(city_state_country("47.470706, -99.704723"))


@csrf_exempt
def user_profile(request):
	if request.method=='GET':
		decoding = JwtMiddleware(request)
		user_data = User.objects.filter(id=decoding['user_id']).values('id','email','first_name','last_name')
		last_seen = User.objects.get(id=decoding['user_id']).last_login 
		b = str(last_seen).split("+")
		a = datetime.strptime(str(b[0]),'%Y-%m-%d %H:%M:%S.%f')
		relative_data = UserProfile.objects.filter(user_id=decoding['user_id'])
		data = []
		if relative_data:
			for i in relative_data:
				data.append({
					"profile_data":{
					"bussiness_type":i.bussiness_type.type_name,
					"bussiness_type_id":i.bussiness_type.id,

					"category":i.category.category_name,
					"category_id":i.category.id,

					"subcategory":i.subcategory.sub_category_name,
					"subcategory_id":i.subcategory.id,
					
					"user_conatct":i.user_conatct,"country":i.country,
					"state":i.state,"city":i.city,
					"zip_code":i.zip_code,"profile_pic":str(i.profile_pic),
					"detail_address":i.detail_address,
					"profile_status":i.profile_status
					},
					"user_data":list(user_data),"last_seen":a })
				return JsonResponse(data,safe=False)
		else:
			return JsonResponse({"user_data":list(user_data),"last_seen":a },safe=False)

		return JsonResponse(data,safe=False)
	elif request.method=='POST':
		decoding = JwtMiddleware(request)
		user_form_data = json.loads(request.body) 
		user_data = User.objects.filter(id=decoding['user_id']).values('id','email','first_name','last_name')	
		print('/////////////////////////',user_form_data)	
		if UserProfile.objects.filter(user_id=decoding['user_id']).exists():
			user_profile = UserProfile.objects.filter(
			user_id = decoding['user_id']).update(
			bussiness_type_id = user_form_data['bussiness_category'],
			category_id = user_form_data['category_s'],
			subcategory_id = user_form_data['subcategory_s'],
			user_conatct = user_form_data['user_conatct'],
			country = user_form_data['country'],
			city = user_form_data['city'],
			state = user_form_data['state'],
			zip_code = user_form_data['zip_code'],
			detail_address = user_form_data['detail_address'],
			profile_status=True
			)
			data = UserProfile.objects.filter(user_id=decoding['user_id']).values()
			return JsonResponse({"success":"Profile updated successfully"})
			# return JsonResponse({
			# 	"data":list(data),
			# 	"user_data":list(user_data)
			# 	},safe=False)
		else:	
			user_profile = UserProfile.objects.create(
				user_id = decoding['user_id'],
				bussiness_type_id = user_form_data['bussiness_category'],
				category_id = user_form_data['category_s'],
				subcategory_id = user_form_data['subcategory_s'],
				user_conatct = user_form_data['user_conatct'],
				country = user_form_data['country'],
				city = user_form_data['city'],
				state = user_form_data['state'],
				zip_code = user_form_data['zip_code'],
				detail_address = user_form_data['detail_address'],
				profile_status = True
				)
			data = UserProfile.objects.filter(user_id=decoding['user_id']).values()
			# return JsonResponse({"data":list(data),
			# 	"user_data":list(user_data)},safe=False)
			return JsonResponse({"success":"Profile created successfully"})
	else:
		return JsonResponse({"data":"Method Not Allowed","last_seen":"No Not At All"},safe=False)

 

@csrf_exempt
def update_password(request):
	decoding = JwtMiddleware(request)
	check = UserProfile.objects.filter(user_id=decoding['user_id'])
	if check:
		update_password = json.loads(request.body)['password']
		user_data = User.objects.filter(id=decoding['user_id']).update(password=make_password(update_password) )		
		return JsonResponse({"data":"Password Updated successfully"},safe=False)
	else:
		return JsonResponse({"data":"Try something new"},safe=False)


def JwtMiddleware(request):	
	token = request.headers['Authorization']
	decoding = jwt.decode(token.split('  ')[0], settings.JWT_SECRET_KEY,algorithms=['HS256'])
	return decoding

																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																														
def verify_token(request):
	try:
		decode = JwtMiddleware(request)
	except:
		return JsonResponse({"error":"login again"})

@csrf_exempt
def user_password_reset(request):
	data = json.loads(request.body)
	try:
		user = User.objects.get(email=data['user_email'])
		number = random.randint(1111,9999)
		otp_instance = PasswordChanged.objects.create(
			user=user,temporary_otp=number
			) 
		message = "You one time password"+'\n'+'Your otp is'+'\n'+str(number)
		msg = EmailMessage('please dont share this otp with anyone', message, to=[data['user_email']], from_email=settings.DEFAULT_FROM_EMAIL)
		msg.send()
		return JsonResponse({"success":data},safe=False)
	except:
		data = {"error":"Email you entered doesn't exists kindly register first"}
		return JsonResponse({"success":data},safe=False)

@csrf_exempt
@api_view(('GET','POST',))
def veryfy_otp(request):
	try:
		otp = PasswordChanged.objects.get(temporary_otp=json.loads(request.body)['otp'],status=False)
		update_otp_status = PasswordChanged.objects.filter(temporary_otp=json.loads(request.body)['otp'],status=False).update(status=True)
		check_user = User.objects.filter(email=otp.user.email,verify_email=True,is_active=True)
		if check_user:
			for i in check_user:
				payload = jwt_payload_handler(i)
				token = jwt.encode(payload, settings.JWT_SECRET_KEY)
				user_details = {}
				user_details['success'] = "success"
				user_details['first_name'] = "%s" % (i.first_name)
				user_details['last_name'] = "%s" % (i.last_name)
				user_details['email'] = "%s" % (i.email)
				user_details['token'] = token
				#print("*/*/*/",user_details)
				return Response(user_details,status=status.HTTP_200_OK)
			else:
				return JsonResponse({"error":"User does not exists"})	
	except:
		return JsonResponse({"error":"improper attempt"})