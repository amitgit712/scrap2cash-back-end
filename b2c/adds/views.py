from django.shortcuts import render
from b2c.models import(
	# CreateGeneralPost,GeneralPostImages,
	CreateIndustrialPost,IndustrialPostImages,
	EnquiryMail,
	)
from admin_dashboard.models import(
	BussinessType,Category,
	Subcategory,ProductType
	)
from rest_auth.models import User,UserProfile
import jwt
import json
from rest_auth.views import JwtMiddleware
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.response import Response
from b2c.serializers import CreateIndustrialPostSerializer
from viit import settings
from django.core.mail import EmailMessage
#import datetime
from datetime import datetime, timedelta

@csrf_exempt
def my_ads(request):
	try:
		decode = JwtMiddleware(request)
	except:
		return JsonResponse({"error":"login again"})
	post = CreateIndustrialPost.objects.filter(created_by=decode['user_id'],user_remove_post=False).values_list("id",flat=True)
	data = []
	for i in post:

		images = IndustrialPostImages.objects.filter(industry_post_id=i).first()
		user_profile = UserProfile.objects.get(user_id=decode['user_id'])
		datas = {
			"post_id":i,
			"product_type":images.industry_post.product_type.id,
			"images":settings.BACKEND_URL+'/media/'+str(images.images),
			"uploaded_on":images.created_at,
			"country":user_profile.country, 
			"state":user_profile.state,
			"selling_price":images.industry_post.selling_price,
			"length":images.industry_post.length,
			"width":images.industry_post.width,
			"quantity":images.industry_post.quantity,
			"weight":images.industry_post.weight,
			"product_detail":images.industry_post.product_description,
			"bargening":images.industry_post.bargening
		}
		data.append(datas)
	return JsonResponse({"success":data})


@csrf_exempt
def delete_ad(request,post_id):
	try:
		decode = JwtMiddleware(request)
	except:
		return JsonResponse({"error":"login again"})
	post = CreateIndustrialPost.objects.filter(created_by=decode['user_id'],id=post_id).update(user_remove_post=True,admin_approval=False)
	return JsonResponse({"success":"post deleted"})

@csrf_exempt
def approoved_ads(request):
	try:
		decode = JwtMiddleware(request)
	except:
		return JsonResponse({"error":"login again"})
	post = CreateIndustrialPost.objects.filter(created_by=decode['user_id'],user_remove_post=False,admin_approval=True).values_list("id",flat=True)
	data = []
	for i in post:
		images = IndustrialPostImages.objects.filter(industry_post_id=i).first()
		user_profile = UserProfile.objects.get(user_id=decode['user_id'])
		datas = {
			"post_id":i,
			"product_type":images.industry_post.product_type.id,
			"images":settings.BACKEND_URL+'/media/'+str(images.images),
			"uploaded_on":images.created_at,
			"country":user_profile.country,
			"state":user_profile.state,
			"selling_price":images.industry_post.selling_price,
			"length":images.industry_post.length,
			"width":images.industry_post.width,
			"quantity":images.industry_post.quantity,
			"weight":images.industry_post.weight,
			"product_detail":images.industry_post.product_description,
			"bargening":images.industry_post.bargening
		}
		data.append(datas)
	return JsonResponse({"success":data})

@csrf_exempt
def unapprooved_ads(request):
	try:
		decode = JwtMiddleware(request)
	except:
		return JsonResponse({"error":"login again"})
	post = CreateIndustrialPost.objects.filter(created_by=decode['user_id'],user_remove_post=False,admin_approval=False).values_list("id",flat=True)
	data = []
	for i in post:
		images = IndustrialPostImages.objects.filter(industry_post_id=i).first()
		user_profile = UserProfile.objects.get(user_id=decode['user_id'])
		datas = {
			"post_id":i,
			"product_type":images.industry_post.product_type.id,
			"images":settings.BACKEND_URL+'/media/'+str(images.images),
			"uploaded_on":images.created_at,
			"country":user_profile.country,
			"state":user_profile.state,
			"selling_price":images.industry_post.selling_price,
			"length":images.industry_post.length,
			"width":images.industry_post.width,
			"quantity":images.industry_post.quantity,
			"weight":images.industry_post.weight,
			"product_detail":images.industry_post.product_description,
			"bargening":images.industry_post.bargening
		}
		data.append(datas)
	return JsonResponse({"success":data})


@csrf_exempt
def update_ads(request):
	try:
		decode = JwtMiddleware(request)
	except:
		return JsonResponse({"error":"login again"})
	post = CreateIndustrialPost.objects.filter(created_by=decode['user_id'],user_remove_post=False,admin_approval=False).values_list("id",flat=True)
	data = []
	for i in post:
		images = IndustrialPostImages.objects.filter(industry_post_id=i).first()
		user_profile = UserProfile.objects.get(user_id=decode['user_id'])
		datas = {
			"post_id":i,
			"product_type":images.industry_post.product_type.id,
			"images":settings.BACKEND_URL+'/media/'+str(images.images),
			"uploaded_on":images.created_at,
			"country":user_profile.country,
			"state":user_profile.state,
			"selling_price":images.industry_post.selling_price,
			"length":images.industry_post.length,
			"width":images.industry_post.width,
			"quantity":images.industry_post.quantity,
			"weight":images.industry_post.weight,
			"product_detail":images.industry_post.product_description,
			"bargening":images.industry_post.bargening
		}
		data.append(datas)
	return JsonResponse({"success":data})