from django.db import models
from admin_dashboard.models import(
	BussinessType,ProductType,
	Category,Subcategory,Material,
	Sub_material,Shape,Units,
	)
from rest_auth.models import User

class CreateIndustrialPost(models.Model):
	created_by = models.ForeignKey(User,on_delete=models.PROTECT,null=True, blank=True)
	bussiness_type = models.ForeignKey(BussinessType,on_delete=models.PROTECT,null=True, blank=True)
	product_type = models.ForeignKey(ProductType,on_delete=models.CASCADE,null=True, blank=True)
	material = models.ForeignKey(Material,on_delete=models.CASCADE,null=True, blank=True)
	sub_material = models.ForeignKey(Sub_material,on_delete=models.CASCADE,null=True, blank=True)
	category_id = models.ForeignKey(Category,on_delete=models.PROTECT,null=True, blank=True)
	sub_category_id = models.ForeignKey(Subcategory,on_delete=models.PROTECT,null=True, blank=True)
	shape = models.ForeignKey(Shape,on_delete=models.PROTECT,null=True, blank=True)
	length = models.CharField(max_length=100,blank=True)
	width = models.CharField(max_length=100,blank=True)
	thickness = models.CharField(max_length=100,blank=True)
	quantity = models.CharField(max_length=100,blank=True)
	weight = models.CharField(max_length=100,blank=True)
	ids = models.CharField(max_length=100,blank=True)
	dimeter = models.CharField(max_length=100,blank=True)
	product_description = models.TextField(blank=True)
	bargening = models.BooleanField(default=False,blank=True)
	selling_price = models.CharField(max_length=20,blank=True)
	units = models.ForeignKey(Units,on_delete=models.PROTECT,null=True, blank=True)
	user_remove_post = models.BooleanField(default=False)
	suspended = models.BooleanField(default=False)
	admin_approval = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True,blank=True)
	updated_at = models.DateTimeField(auto_now=True,blank=True)

	def __str__(self):
		if not self.material:
			return 'None'
		else:
			return self.material.material_type

class IndustrialPostImages(models.Model):
	industry_post = models.ForeignKey(CreateIndustrialPost,on_delete=models.CASCADE,null=True, blank=True)
	images = models.ImageField(upload_to="images/industry",blank=True)
	created_at = models.DateTimeField(auto_now_add=True,blank=True)
	updated_at = models.DateTimeField(auto_now=True,blank=True)

	def __str__(self):
		return str(self.industry_post)

class SellerData(models.Model):
	user = models.ForeignKey(User,on_delete=models.PROTECT,null=True, blank=True)
	username = models.CharField(max_length=100,blank=True)
	email = models.EmailField(max_length=100,blank=True)
	contact = models.CharField(max_length=100,blank=True)
	country = models.CharField(max_length=100,blank=True)
	state = models.CharField(max_length=100,blank=True)
	city = models.CharField(max_length=100,blank=True)
	zip_code = models.CharField(max_length=100,blank=True)
	detail_address = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True,blank=True)
	updated_at = models.DateTimeField(auto_now=True,blank=True)

	def __str__(self):
		return str(self.user)


class ScrapPrice(models.Model):
	name = models.CharField(max_length=100)
	price = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True,blank=True)
	def __str__(self):
		return str(self.name)

class EnquiryMail(models.Model):
	requested_by = models.CharField(max_length=100)
	requested_to = models.CharField(max_length=100)
	post_id  = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True,blank=True)
	updated_at = models.DateTimeField(auto_now=True,blank=True)

	def __str__(self):
		return self.requested_by

# class PostReview(models.Model):
# 	post = models.ForeignKey(CreatePost,on_delete=models.PROTECT)
# 	ratings = models.IntegerField(blank=True)
# 	comments = models.TextField(blank=True)
# 	def __str__(self):
# 		return str(self.ratings)
