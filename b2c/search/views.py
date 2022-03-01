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
from viit import settings
from django.core.mail import EmailMessage
#import datetime
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.views.generic import ListView
from django.db.models import Q
from itertools import chain

@csrf_exempt
def search(request):
	try:
		decoding = JwtMiddleware(request)
	except:
		return JsonResponse({"token_error":"login again"})
	d = json.loads(request.body.decode('utf-8').lower())
	if request.method == 'POST':
		material=d.get('material')
		lenght=d.get('lenght')
		if not lenght:
			lenght = 'none'
		width=d.get('width')
		if not width:
			width = 'none'
		weight=d.get('weight')
		if not weight:
			weight = 'none'
		thickness=d.get('thickness')
		if not thickness:
			thickness = 'none'
		sid=d.get('sid')
		dimeter=d.get('dimeter')
		data = []
		posts = CreateIndustrialPost.objects.filter(
		Q(material__material_type=material,admin_approval=True,user_remove_post=False)
		|Q(length__gte=lenght,admin_approval=True,user_remove_post=False)
		|Q(width__gte=width,admin_approval=True,user_remove_post=False)
		|Q(thickness__gte=thickness,admin_approval=True,user_remove_post=False)
		|Q(ids=sid,admin_approval=True,user_remove_post=False)
		|Q(dimeter=dimeter,admin_approval=True,user_remove_post=False)
		|Q(weight__gte=weight,admin_approval=True,user_remove_post=False)).order_by('-id').values()
		for i in posts:
			category = Category.objects.filter(id=i['category_id_id']).values()
			images = IndustrialPostImages.objects.filter(industry_post_id=i['id']).order_by('-id').values()
			user_detail = User.objects.filter(id=i['created_by_id']).values(
			"id","last_login","first_name","last_name",
			"date_joined","email")
			user_profile = user_profile = UserProfile.objects.filter(user_id=i['created_by_id']).values()
			data.append({
			'post_id':i['id'],'created_by_id':i['created_by_id'],
			'category_type_id':i['bussiness_type_id'],'product_type_id':i['product_type_id'],
			'category_id':i['category_id_id'],'sub_category_id':i['sub_category_id_id'],
			'length':i['length'],
			'quantity':i['quantity'],'width':i['width'],'weight':i['weight'],'thickness':i['thickness'],
			'product_description':i['product_description'],'bargening':i['bargening'],
			'selling_price':i['selling_price'],"created_at":i['created_at'],"updated_at":i['updated_at'],
			"image":list(images),"image_prefix":settings.BACKEND_URL+'/media/',
			"category":list(category),"user_detals":list(user_detail),"user_profile":list(user_profile),
			})
		return JsonResponse(data,safe=False)
	else:
		return HttpResponse("method not allowed")
