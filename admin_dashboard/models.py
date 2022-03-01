from django.db import models
from rest_auth.models import User


class BussinessType(models.Model):
	created_by = models.ForeignKey(User,on_delete=models.PROTECT,null=True, blank=True)
	type_name = models.CharField(max_length=10000,blank=True)
	status = models.BooleanField(default=True,blank=True)
	created_at = models.DateTimeField(auto_now_add=True,blank=True)
	updated_at = models.DateTimeField(auto_now=True,blank=True)
	def save(self, *args, **kwargs):
		self.type_name = self.type_name.lower()
		return super(BussinessType, self).save(*args, **kwargs)

	def __str__(self): 
		return self.type_name 

class Category(models.Model):
	bussiness_type = models.ForeignKey(BussinessType,on_delete=models.PROTECT,null=True, blank=True)
	category_name = models.CharField(max_length=1000,blank=True,null=True)
	image = models.FileField(upload_to='images/category',blank=True)
	status = models.BooleanField(default=True,blank=True)
	created_at = models.DateTimeField(auto_now_add=True,blank=True)
	updated_at = models.DateTimeField(auto_now=True,blank=True)
	def save(self, *args, **kwargs):
		self.category_name = self.category_name.lower()
		return super(Category, self).save(*args, **kwargs)
	def __str__(self):
		return self.category_name

class Subcategory(models.Model):
	category = models.ForeignKey(Category,on_delete=models.PROTECT,null=True, blank=True)
	sub_category_name = models.CharField(max_length=1000,blank=True)
	status = models.BooleanField(default=True,blank=True)
	created_at = models.DateTimeField(auto_now_add=True,blank=True)
	updated_at = models.DateTimeField(auto_now=True,blank=True)
	def save(self, *args, **kwargs):
		self.sub_category_name = self.sub_category_name.lower()
		return super(Subcategory, self).save(*args, **kwargs)
	def __str__(self):
		return self.sub_category_name



class ProductType(models.Model):
	product_type = models.CharField(max_length=1000,blank=True)
	status = models.BooleanField(default=True,blank=True)
	created_at = models.DateTimeField(auto_now_add=True,blank=True)
	updated_at = models.DateTimeField(auto_now=True,blank=True)
	def save(self, *args, **kwargs):
		self.product_type = self.product_type.lower()
		return super(ProductType, self).save(*args, **kwargs)
	def __str__(self):
		return self.product_type

class Units(models.Model):
	unit_type = models.CharField(max_length=1000,blank=True)
	status = models.BooleanField(default=True,blank=True)
	created_at = models.DateTimeField(auto_now_add=True,blank=True)
	updated_at = models.DateTimeField(auto_now=True,blank=True)
	def save(self, *args, **kwargs):
		self.unit_type = self.unit_type.lower()
		return super(Units, self).save(*args, **kwargs)
	def __str__(self):
		return self.unit_type

class Material(models.Model):
	material_type = models.CharField(max_length=1000,blank=True)
	status = models.BooleanField(default=True,blank=True)
	created_at = models.DateTimeField(auto_now_add=True,blank=True)
	updated_at = models.DateTimeField(auto_now=True,blank=True)
	def save(self, *args, **kwargs):
		self.material_type = self.material_type.lower()
		return super(Material, self).save(*args, **kwargs)
	def __str__(self):
		return self.material_type

class Sub_material(models.Model):
	material = models.ForeignKey(Material,on_delete=models.PROTECT,null=True, blank=True)
	grade = models.CharField(max_length=1000,blank=True)
	status = models.BooleanField(default=True,blank=True)
	created_at = models.DateTimeField(auto_now_add=True,blank=True)
	updated_at = models.DateTimeField(auto_now=True,blank=True)
	def save(self, *args, **kwargs):
		self.grade = self.grade.lower()
		return super(Sub_material, self).save(*args, **kwargs)
	def __str__(self):
		return self.grade

class Shape(models.Model):
	shape_type = models.CharField(max_length=1000,blank=True)
	status = models.BooleanField(default=True,blank=True)
	created_at = models.DateTimeField(auto_now_add=True,blank=True)
	updated_at = models.DateTimeField(auto_now=True,blank=True)
	def save(self, *args, **kwargs):
		self.shape_type = self.shape_type.lower()
		return super(Shape, self).save(*args, **kwargs)
	def __str__(self):
		return self.shape_type