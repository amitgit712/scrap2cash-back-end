from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from rest_auth.models import UserProfile,User
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from b2c.models import(
	CreateIndustrialPost,
	IndustrialPostImages
	)
from admin_dashboard.models import(
	BussinessType,Category,
	Subcategory,ProductType
	)
from django.core.mail import EmailMessage
from viit import settings

def admin_login(request):
	if request.method=='POST':
		email = request.POST.get('email')
		password =  request.POST.get('password')
		user = authenticate(request,username=email,password=password)
		if user is not None:
			login(request,user)
			if request.user.is_superuser:
				return HttpResponseRedirect("/admin_dashboard/admin_dashboard/")
			else:
				return HttpResponseRedirect("https://scrap2cash.in")
		else:
			context = {
				"error":'invalid credentials',
			}
			return render(request,"admin_dashboard/login.html",context)
	else:
		return render(request,"admin_dashboard/login.html")


def logout_view(request):
	logout(request)
	return HttpResponseRedirect("/admin_dashboard/admin_login/")


@login_required
def admin_dashboard(request):
	user = request.user
	user_profile = "dsf"
	recently_added = CreateIndustrialPost.objects.filter(user_remove_post=False,admin_approval=False,suspended=False)

	context = {
		"admin_data":user.admin_image_link,
		"recently_added":recently_added
	}
	return render(request,"admin_dashboard/index.html",context)

@login_required
def view_post(request,post_id):
	if request.user.is_superuser:
		post_details = CreateIndustrialPost.objects.filter(id=post_id)
		for i in post_details:
			images = IndustrialPostImages.objects.filter(industry_post_id=i.id)
			profile = UserProfile.objects.filter(user_id=i.created_by_id)
			for j in profile:
				context = {
					"post_details":i,
					"images":images,
					"profile":j,
				}
		return render(request,"admin_dashboard/post_detail.html",context)
	else:
		return HttpResponseRedirect("https://scrap2cash.in")

@login_required
def approve_post(request,post_id):
	if request.user.is_superuser:
		posts = CreateIndustrialPost.objects.filter(id=post_id).update(admin_approval=True)
		return redirect("admin_dashboard:all_unapprove_post")
	else:
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'),context={"error":"You are not allowed to access"})


@login_required
def suggest_changes(request,post_id):
	if request.user.is_superuser:
		posts = CreateIndustrialPost.objects.filter(id=post_id).update(admin_approval=True)
		post_data = CreateIndustrialPost.objects.filter(id=post_id)
		for i in post_data:
			user_profile =  UserProfile.objects.filter(user_id=i.created_by_id)
			for j in user_profile:
				message = "Your post has been approved post details are as bellow:\n"+'Post Id:'+ str(post_id)+'\n'+'Product Name: '+str(i.product_brand_name)
				msg = EmailMessage(
					'Thanks for using scarp2cash we assure you greate deal',
					message,to=[j.user.email],
					from_email=settings.DEFAULT_FROM_EMAIL

					)
				msg.send()
			return HttpResponseRedirect("/admin_dashboard/admin_dashboard/")
	else:
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'),context={"error":"You are not allowed to access"})


@login_required
def suspend_post(request,post_id):
	if request.user.is_superuser:
		posts = CreateIndustrialPost.objects.filter(id=post_id).update(admin_approval=False,suspended=True)
		return redirect('admin_dashboard:all_suspended_post')
	else:
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'),context={"error":"You are not allowed to access"})



@login_required
def admin_index(request):
	return render(request,"admin_dashboard/index.html")

@login_required
def users(request):
	users = User.objects.all()
	return render(request,"admin_dashboard/users.html",{'users':users})

@login_required
def user_deatail(request,id):
	try:
		user_detail = UserProfile.objects.get(user_id=id)
		user_detail_error=None
	except:
		user_detail_error = "This User not created his profile."
		user_detail=None
	return render(request,"admin_dashboard/user_detail.html",{'user_detail':user_detail,'user_detail_error':user_detail_error})

@login_required
def approve(request):
	approve_post = CreateIndustrialPost.objects.filter(admin_approval=True).count()
	return render(request,"admin_dashboard/index.html",{'approve_post':approve_post})
@login_required
def all_approve_post(request):
	approve_post = IndustrialPostImages.objects.filter(industry_post__admin_approval=True,industry_post__user_remove_post=False,industry_post__suspended=False)
	return render(request,"admin_dashboard/all_approve_post.html",{'approve_post':approve_post})
@login_required
def unapprove(request,id):
	if request.user.is_superuser:
		posts = CreateIndustrialPost.objects.filter(id=id).update(admin_approval=False)
		return redirect('admin_dashboard:all_approve_post')
	else:
		return redirect('/')
@login_required
def all_unapprove_post(request):
	unapproved_post = IndustrialPostImages.objects.filter(industry_post__admin_approval=False,industry_post__user_remove_post=False,industry_post__suspended=False)
	return render(request,"admin_dashboard/all_unapprove_post.html",{'unapproved_post':unapproved_post})
@login_required
def all_suspended_post(request):
	suspended_post = IndustrialPostImages.objects.filter(industry_post__admin_approval=False,industry_post__user_remove_post=False,industry_post__suspended=True)
	return render(request,"admin_dashboard/suspended_post.html",{'suspended_post':suspended_post})

@login_required
def unsuspend_post(request,id):
	if request.user.is_superuser:
		posts = CreateIndustrialPost.objects.filter(id=id).update(admin_approval=False,suspended=False)
		return redirect('admin_dashboard:all_unapprove_post')
	else:
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'),context={"error":"You are not allowed to access"})
