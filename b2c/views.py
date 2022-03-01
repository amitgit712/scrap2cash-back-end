
from django.shortcuts import render
from b2c.models import(
	# CreateGeneralPost,GeneralPostImages,
	CreateIndustrialPost,IndustrialPostImages,
	EnquiryMail,ScrapPrice
	)

from admin_dashboard.models import(
	BussinessType,Category,
	Subcategory,ProductType,Material,Sub_material,Shape,Units
	)

from rest_auth.models import User,UserProfile
import jwt
import json
from django.shortcuts import get_object_or_404
from rest_auth.views import JwtMiddleware
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.response import Response
from b2c.serializers import CreateIndustrialPostSerializer
from viit import settings
from django.template.loader import get_template
from django.core.mail import EmailMessage
#import datetime
from datetime import datetime, timedelta
from django.urls import reverse

@csrf_exempt
def send_form_attributes(request): #for category type
	try:
		decoding = JwtMiddleware(request)
	except:
		return JsonResponse({"token_error":"login again"})

	if request.method=='GET':
		data = []
		category_type=BussinessType.objects.all().values()
		for i in category_type:
			data.append({"id":i['id'],"category_type":i['type_name']})
		return JsonResponse(data,safe=False)
	else:
		return JsonResponse({"No":"something cool is comming"},safe=False)

@csrf_exempt
def get_category(request,BussinessTypeId):
	data = []
	category=Category.objects.filter(bussiness_type_id=BussinessTypeId).values()
	for i in category:
		data.append({"id":i['id'],"category":i['category_name']})
	return JsonResponse(data,safe=False)

@csrf_exempt
def get_post_data(request,id):
	try:
		decoding = JwtMiddleware(request)
	except:
		return JsonResponse({"token_error":"login again"})
	data = []
	post=IndustrialPostImages.objects.filter(industry_post__id=id)
	for i in post:
		data.append({
			"id":i.industry_post.id,
			"product_type":i.industry_post.product_type.product_type,
			"material":i.industry_post.material.material_type,
			"sub_material":i.industry_post.sub_material.grade,
			"shape":i.industry_post.shape.shape_type,
			"length":i.industry_post.length,
			"dimeter":i.industry_post.dimeter,
			"ids":i.industry_post.ids,
			"width":i.industry_post.width,
			"weight":i.industry_post.weight,
			"thickness":i.industry_post.thickness,
			"quantity":i.industry_post.quantity,
			"product_description":i.industry_post.product_description,
			"bargening":i.industry_post.bargening,
			"selling_price":i.industry_post.selling_price,
			"images":settings.BACKEND_URL+'/media/'+str(i.images)
			})
	return JsonResponse(data,safe=False)

@csrf_exempt
def all_category(request):
	data = []
	category=Category.objects.all().values()
	for i in category:
		data.append({"id":i['id'],"category":i['category_name']})
	return JsonResponse(data,safe=False)


@csrf_exempt
def all_subcategory(request):
	try:
		decoding = JwtMiddleware(request)
	except:
		return JsonResponse({"token_error":"login again"})

	data = []
	subcategory=Subcategory.objects.all().values()
	for i in subcategory:
		data.append({"id":i['id'],"subcategory":i['sub_category_name']})
	return JsonResponse(data,safe=False)

@csrf_exempt
def get_subcategory(request,categoryId):
	try:
		decoding = JwtMiddleware(request)
	except:
		return JsonResponse({"token_error":"login again"})
	data = []
	subcategory=Subcategory.objects.filter(category_id=categoryId).values()
	for i in subcategory:
		data.append({"id":i['id'],"subcategory":i['sub_category_name']})
	return JsonResponse(data,safe=False)

@csrf_exempt
def get_submaterial(request,materialId):
	try:
		decoding = JwtMiddleware(request)
	except:
		return JsonResponse({"token_error":"login again"})
	data = []
	submaterial=Sub_material.objects.filter(material_id=materialId).values()
	for i in submaterial:
		data.append({"id":i['id'],"grade":i['grade']})
	return JsonResponse(data,safe=False)


@csrf_exempt
def get_producttype(request):
	# print("***************",BussinessTypeId)
	try:
		decoding = JwtMiddleware(request)
	except:
		return JsonResponse({"token_error":"login again"})

	data = []
	product_type=ProductType.objects.all().values()
	for i in product_type:
		data.append({"id":i['id'],"product_type":i['product_type']})
	return JsonResponse(data,safe=False)

@csrf_exempt
def get_material(request):
	# print("***************",BussinessTypeId)
	try:
		decoding = JwtMiddleware(request)
	except:
		return JsonResponse({"token_error":"login again"})

	data = []
	material_type=Material.objects.all().values()
	for i in material_type:
		data.append({"id":i['id'],"material_type":i['material_type']})
	return JsonResponse(data,safe=False)


@csrf_exempt
def get_shape(request):
	try:
		decoding = JwtMiddleware(request)
	except:
		return JsonResponse({"token_error":"login again"})
	data = []
	shape_type  = Shape.objects.all().values()
	for i in shape_type:
		data.append({"id":i['id'],"shape_type":i['shape_type']})
	return JsonResponse(data,safe=False)

@csrf_exempt
def get_unit(request):
	try:
		decoding = JwtMiddleware(request)
	except:
		return JsonResponse({"token_error":"login again"})
	data = []
	unit_type  = Units.objects.all().values()
	for i in unit_type:
		data.append({"id":i['id'],"unit_type":i['unit_type']})
	return JsonResponse(data,safe=False)


@csrf_exempt
def get_formdata(request,BussinessTypeId):
	data = []
	category=BussinessType.objects.filter(id=BussinessTypeId).values()
	for i in category:
		if i['type_name']=='Industry':
			d = CreateIndustrialPost.objects.all().values()
			for j in d:
				data.append({"Industry":j})
	return JsonResponse(data,safe=False)


@csrf_exempt
def create_post(request):
	try:
		decoding = JwtMiddleware(request)
	except:
		return JsonResponse({"token_error":"login again"})
	data = json.loads(request.body.decode('utf-8').lower())
	user_profile_status = UserProfile.objects.get(user_id=decoding['user_id'],profile_status=True)

	if data['req_material']:
		ctx = {
			"material_name" : data['req_material'],
			"created_by" : user_profile_status.user.email,
			"admin_url" : reverse('admin_dashboard:admin_login'),
		}
		request_material(ctx)
	if data['req_grade']:
		ctx2 = {
		"submaterial_name" : data['req_grade'],
		"created_by" : user_profile_status.user.email,
		"admin_url" : reverse('admin_dashboard:admin_login'),
		}
		request_submaterial(ctx2)
	if data['req_shape']:
		ctx3 = {
		"req_name" : data['req_shape'],
		"created_by" : user_profile_status.user.email,
		"admin_url" : reverse('admin_dashboard:admin_login'),
		}
		request_shape(ctx3)

	if data['bargening']=='':
		bargening = False
	else:
		bargening =True

	if user_profile_status:
		create_post = CreateIndustrialPost.objects.create(
			created_by_id = decoding['user_id'],
			bussiness_type_id = user_profile_status.bussiness_type_id,#data['select_category_type'],
			product_type_id = data['select_product_type'],
			category_id_id = user_profile_status.category_id,#data['select_category'],
			sub_category_id_id = user_profile_status.subcategory_id,#data['select_subcategory'],
			material_id = data['material'],
			sub_material_id = data['grade'],
			shape_id =  data['shape'],
			length = data['length'],
			width = data['width'],
			thickness = data['thickness'],
			quantity = data['quantity'],
			weight = data['weight'],
			ids = data['ids'],
			dimeter = data['dimeter'],
			product_description = data['product_description'],
			units_id = data['unit'],
			bargening = bargening,
			selling_price = data['selling_price']
			)
		ctx = {
			'created_by': user_profile_status.user.email
			}
		create_email(ctx)
		return JsonResponse({"response":list(CreateIndustrialPost.objects.filter(id=create_post.id).values())},safe=False)
	else:
		return JsonResponse({"error":"error"})

def create_email(ctx):
	subject = 'Post added by {}.'.format(ctx['created_by'])
	email_temp = get_template(
		'email_temp/created_post_admin.html').render(ctx)
	msg = EmailMessage(
		subject,
		email_temp,
		settings.DEFAULT_FROM_EMAIL,
		[settings.DEFAULT_FROM_EMAIL,],
		)
	msg.content_subtype = "html"
	msg.send()
	pass

@csrf_exempt
def update_post(request,id):
	try:
		decoding = JwtMiddleware(request)
	except:
		return JsonResponse({"token_error":"login again"})
	# print("/*/*/*/*/*/*/ request",request.body.split(b'images'))
	data = json.loads(request.body.decode('utf-8').lower())
	user_profile_status = UserProfile.objects.get(user_id=decoding['user_id'],profile_status=True)
	if data['material']:
		ctx = {
			"material_name" : data['material'],
			"created_by" : user_profile_status.user.email,
			"admin_url" : reverse('admin_dashboard:admin_login'),
		}
		request_material(ctx)
	if data['req_grade']:
		ctx2 = {
		"submaterial_name" : data['grade'],
		"created_by" : user_profile_status.user.email,
		"admin_url" : reverse('admin_dashboard:admin_login'),
		}
		request_submaterial(ctx2)
	if data['req_shape']:
		ctx3 = {
		"req_name" : data['shape'],
		"created_by" : user_profile_status.user.email,
		"admin_url" : reverse('admin_dashboard:admin_login'),
		}
		request_shape(ctx3)
	if data['bargening']=='':
		bargening = False
	else:
		bargening =True
	if user_profile_status:
		update_post = CreateIndustrialPost.objects.filter(id=id).update(
			created_by_id = decoding['user_id'],
			bussiness_type_id = user_profile_status.bussiness_type_id,#data['select_category_type'],
			product_type_id = data['select_product_type'],
			category_id_id = user_profile_status.category_id,#data['select_category'],
			sub_category_id_id = user_profile_status.subcategory_id,#data['select_subcategory'],
			material_id = data['material'],
			sub_material_id = data['grade'],
			shape_id =  data['shape'],
			length = data['length'],
			width = data['width'],
			thickness = data['thickness'],
			quantity = data['quantity'],
			weight = data['weight'],
			ids = data['ids'],
			dimeter = data['dimeter'],
			product_description = data['product_description'],
			bargening = bargening,
			selling_price = data['selling_price'],
			units_id = data['unit'],
			admin_approval = False
			)
		ctx = {
			'created_by': user_profile_status.user.email

		}
		update_email(ctx)
		return JsonResponse({"response":"successfully updated"})
	else:
		return JsonResponse({"error":"error"})

def update_email(ctx):
	subject = 'Post updated by {}.'.format(ctx['created_by'])
	email_temp = get_template(
		'email_temp/update_post_admin.html').render(ctx)
	msg = EmailMessage(
		subject,
		email_temp,
		settings.DEFAULT_FROM_EMAIL,
		[settings.DEFAULT_FROM_EMAIL,],
		)
	msg.content_subtype = "html"
	msg.send()
	pass
def request_material(ctx):
	subject = 'New material request by {}.'.format(ctx['created_by'])
	email_temp = get_template(
		'email_temp/req_material_admin.html').render(ctx)
	msg = EmailMessage(
		subject,
		email_temp,
		settings.DEFAULT_FROM_EMAIL,
		[settings.DEFAULT_FROM_EMAIL,],
		)
	msg.content_subtype = "html"
	msg.send()
	pass


def request_submaterial(ctx2):
	subject = 'New grade request by {}.'.format(ctx2['created_by'])
	email_temp = get_template(
		'email_temp/req_submaterial_admin.html').render(ctx2)
	msg = EmailMessage(
		subject,
		email_temp,
		settings.DEFAULT_FROM_EMAIL,
		[settings.DEFAULT_FROM_EMAIL,]
		,)
	msg.content_subtype = "html"
	msg.send()
	pass

def request_shape(ctx3):
	subject = 'New shape request by {}.'.format(ctx3['created_by'])
	email_temp = get_template(
		'email_temp/req_shape_admin.html').render(ctx3)
	msg = EmailMessage(
		subject,
		email_temp,
		settings.DEFAULT_FROM_EMAIL,
		[settings.DEFAULT_FROM_EMAIL,],)
	msg.content_subtype = "html"
	msg.send()
	pass

@csrf_exempt
def upload_files(request):
	try:
		decoding = JwtMiddleware(request)
	except:
		return JsonResponse({"token_error":"login again"})
	post_id = CreateIndustrialPost.objects.filter(created_by_id=decoding['user_id']).latest('id')
	for i in request.FILES.getlist('images')[:5]:
		IndustrialPostImages.objects.create(
		industry_post_id = post_id.id,
		images = i
		)
	return JsonResponse({"Success":"uploaded"})



@csrf_exempt
def update_files(request,id):
	try:
		decoding = JwtMiddleware(request)
	except:
		return JsonResponse({"token_error":"login again"})
	for i in request.FILES.getlist('images')[:5]:
		update_old_images = IndustrialPostImages.objects.update_or_create(industry_post_id=id,images=i)
	return JsonResponse({"Success":"updated"})


@csrf_exempt
def home_data(request):
	#decoding = JwtMiddleware(request)
	data = []
	category = Category.objects.all().values("id","bussiness_type_id","category_name","image")
	for i in category:
		data.append({"id":i['id'],"bussiness_type_id":i['bussiness_type_id'],"category_name":i['category_name'],"image":settings.BACKEND_URL+'/media/'+i['image']})
	return JsonResponse(data,safe=False)

@csrf_exempt
def recent_post(request):
	#decoding = JwtMiddleware(request)
	data = []
	posts = CreateIndustrialPost.objects.filter(
		admin_approval=True,user_remove_post=False
		).order_by('-id').values()
	for i in posts:
		category = Category.objects.filter(id=i['category_id_id']).values()
		images = IndustrialPostImages.objects.filter(industry_post_id=i['id']).order_by('-id').values()
		user_detail = User.objects.filter(id=i['created_by_id']).values(
			"id","last_login","first_name","last_name",
			"date_joined","email")
		user_profile = user_profile = UserProfile.objects.filter(user_id=i['created_by_id']).values()
		data.append({
			'post_id':i['id'],'created_by_id':i['created_by_id'],
			'product_type_id':i['product_type_id'],
			'category_id':i['category_id_id'],'sub_category_id':i['sub_category_id_id'],
			'length':i['length'],
			'quantity':i['quantity'],'width':i['width'],'weight':i['weight'],
			'product_description':i['product_description'],'bargening':i['bargening'],
			'selling_price':i['selling_price'],"created_at":i['created_at'],"updated_at":i['updated_at'],
			"image":list(images),"image_prefix":settings.BACKEND_URL+'/media/',
			"category":list(category),"user_detals":list(user_detail),"user_profile":list(user_profile),
			# "image":settings.BACKEND_URL+'/media/'+j['images'],
			})
	return JsonResponse(data,safe=False)





@csrf_exempt
def category_wise(request,catId):
	#decoding = JwtMiddleware(request)
	data = []
	posts = CreateIndustrialPost.objects.filter(
		admin_approval=True,user_remove_post=False,category_id=catId
		).order_by('-id').values()
	# print("*/*/*/*/*/*/*/ posts",posts)
	for i in posts:
		# print("*/*/*/*/*/i",i)
		category = Category.objects.filter(id=i['category_id_id']).values()
		# print("*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/",i)
		images = IndustrialPostImages.objects.filter(industry_post_id=i['id']).order_by('-id').values()
		user_detail = User.objects.filter(id=i['created_by_id']).values(
			"id","last_login","first_name","last_name",
			"date_joined","email")
		user_profile = user_profile = UserProfile.objects.filter(user_id=i['created_by_id']).values()
		data.append({
			'post_id':i['id'],'created_by_id':i['created_by_id'],
			'product_type_id':i['product_type_id'],
			'category_id':i['category_id_id'],'sub_category_id':i['sub_category_id_id'],
			'length':i['length'],
			'quantity':i['quantity'],'width':i['width'],'weight':i['weight'],
			'product_description':i['product_description'],'bargening':i['bargening'],
			'selling_price':i['selling_price'],"created_at":i['created_at'],"updated_at":i['updated_at'],
			"image":list(images),"image_prefix":settings.BACKEND_URL+'/media/',
			"category":list(category),"user_detals":list(user_detail),"user_profile":list(user_profile),
			# "image":settings.BACKEND_URL+'/media/'+j['images'],
			})
	return JsonResponse(data,safe=False)


def post_detail_view(request,postId):
	try:
		decoding = JwtMiddleware(request)
	except:
		return JsonResponse({"token_error":"login again"})
	data = []
	post_detail = CreateIndustrialPost.objects.filter(id=postId).values()
	for i in post_detail:
		print("//////////",i)
		cataegory_type = BussinessType.objects.filter(id=i['bussiness_type_id']).values()
		for k in cataegory_type:
			print("")
		category = Category.objects.filter(id=i['category_id_id']).values()
		for l in category:
			print("")
		subcategory =Subcategory.objects.filter(id=i['sub_category_id_id']).values()
		for m in subcategory:
			print("")
		product_type=ProductType.objects.filter(id=i['product_type_id']).values()
		for p in product_type:
			print("")
		material=Material.objects.filter(id=i['material_id']).values()
		for d in material:
			print("")
		images = IndustrialPostImages.objects.filter(industry_post_id=i['id']).values()
		image_list = []
		for image in images:
			image_list.append(
					{"images":{"id":image['id'],"industry_post_id":image['industry_post_id'],
					"images":settings.BACKEND_URL+'/media/'+image['images']}
					})
		user_detail = User.objects.filter(id=i['created_by_id']).values(
			"id","last_login","first_name","last_name",
			"date_joined","email")
		for j in user_detail:
			print("test")
			user_profile = UserProfile.objects.filter(user_id=j['id']).values()

			for c in user_profile:
				data.append({
					"post_data":i,"category_type":k,"category":l,"product_type":p,
					"subcategory":m,"user_details":j,"user_profile":c,"material":d,
					"images":image_list
					})
	return JsonResponse(data,safe=False)


def check_last_mail(request,requested_by_id,requested_to_id,post_id):
	time_threshold = datetime.now() - timedelta(minutes=1)
	enq_mail = EnquiryMail.objects.filter(
		requested_by=requested_by_id,requested_to=requested_to_id,
		post_id=post_id,created_at__lt=time_threshold).values()
	enq_updated_mail = EnquiryMail.objects.filter(
		requested_by=requested_by_id,requested_to=requested_to_id,
		post_id=post_id,updated_at__lt=time_threshold).values()
	if enq_mail is not None:
		return enq_mail#HttpResponse("Your attempt is over you can try after 24 hours")
	elif enq_updated_mail is not None:
		return enq_updated_mail#HttpResponse("Your attempt is over you can try after 24 hours")
	else:
		pass

def mail_product_requirements(request,postId):
	try:
		decoding = JwtMiddleware(request)
	except:
		return JsonResponse({"token_error":"login again"})
	post_data = CreateIndustrialPost.objects.filter(id=postId).values()
	# print('//////////////////////////////',post_data)
	for i in post_data:
		check_mail = check_last_mail(request,decoding['user_id'],i['created_by_id'],i['id'])
		if check_mail:
			return JsonResponse({"error":"Sorry you can try again after 24 hours again"})
		else:
			pass
		product_info = 'product Type id : '+str(i['product_type_id'])+'\n'+'Quantity : '+str(i['quantity'])+'\n'+'Selling Price  ₹ '+str(i['selling_price'])+'\n'+'Uploaded on :'+str(i['created_at'])
		vendor_email = User.objects.filter(id=i['created_by_id']).values("id","first_name","last_name","email")

		vendor_details = UserProfile.objects.filter(user_id=i['created_by_id']).values()

		for vd in vendor_details:
			v_d = User.objects.filter(id=decoding['user_id']).values()
			for k in v_d:
				v_details = 'Vendor Name :'+ str(k['first_name']) + ' '+str(k['last_name'])+'\n'+'Contact Number : '+str(vd['user_conatct'])+'\n'+'Email :'+k['email']
				for v in vendor_email:
					message = 'Hey  '+v['first_name'] +' ' + 'you have an enquirey for your product listed on scrap2cash.in'+'\n\n'+product_info + '\n\n'+ 'Vendor details Who is looking for your products'+'\n' + v_details
					msg = EmailMessage(
						'Product  enquiry from scrap2cash.in ',
						message,to=[v['email']],
						from_email=settings.DEFAULT_FROM_EMAIL
						)
					msg.send()

					message = 'Hey  '+ ' ' +k['first_name'] +' ' + 'we have sent mail on behalf of you to'+' '+ v['first_name']+' '+v['last_name']+' '+'for your intrest in product listed on scrap2cash.in'+' '+'\n\n'+product_info
					msg = EmailMessage(
						'Thanks for using scarp2cash we assure you greate deal',
						message,to=[decoding['email']],
						from_email=settings.DEFAULT_FROM_EMAIL
						)
					msg.send()

				mail_record = EnquiryMail.objects.filter(
					requested_by=decoding['user_id'],requested_to=i['created_by_id'],
					post_id=postId).update_or_create(
					requested_by=decoding['user_id'],
					requested_to=i['created_by_id'],
					post_id=postId
					)
				return JsonResponse({"success":"Mail send successfully"})
		return JsonResponse({"error":"Mail server is down if problem persist "})



@csrf_exempt
def scrapdata(request):
	data = []
	datas = ScrapPrice.objects.all().values()
	for i in datas:
		data.append({"name":i['name'],"price":i['price']})
	return JsonResponse(data,safe=False)



class CreatePostViewSet(viewsets.ModelViewSet):
	queryset = CreateIndustrialPost.objects.all()
	serializer_class = CreateIndustrialPostSerializer
	def post(self,request,*args,**kwargs):
		decoding = JwtMiddleware(request)
		create_post = CreateIndustrialPost.objects.create(
		created_by_id = decoding['user_id'],

		bussiness_type = request.data['bussiness_type_id'],
		product_type_id = request.data['product_type_id'],
		ids = request.data['ids'],
		dimeter = request.data['dimeter'],
		category_id = request.data['select_category'],
		sub_category_id = request.data['select_subcategory'],
		shape = request.data['shape'],
		quantity = request.data['quantity'],
		product_description = request.data['product_description'],
		bargening = request.data['bargening'],
		selling_price = request.data['selling_price']
		)
		upload_images = IndustrialPostImages.objects.create(
		industry_post_id = create_post.id,
		images = request.data['image1']
		)
