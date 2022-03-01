from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

 

class User(AbstractUser):
    username = models.CharField(max_length=100,blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    verify_email = models.BooleanField(default=False)
    admin_image_link = models.CharField(max_length=2000,blank=True)
    #is_active = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']
    
    def save(self, *args, **kwargs): 
    	self.email = self.email.lower()
    	self.first_name = self.first_name.lower()
    	self.last_name = self.last_name.lower()
    	return super(User, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.email)

class UserProfile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	bussiness_type = models.ForeignKey('admin_dashboard.BussinessType',on_delete=models.PROTECT,null=True, blank=True)
	category = models.ForeignKey('admin_dashboard.Category',on_delete=models.PROTECT,null=True, blank=True)
	subcategory = models.ForeignKey('admin_dashboard.Subcategory',on_delete=models.PROTECT,null=True, blank=True)
	user_conatct = models.CharField(max_length=1000,blank=True)
	country = models.CharField(max_length=1000,blank=True)
	state = models.CharField(max_length=1000,blank=True)
	city = models.CharField(max_length=1000,blank=True)
	zip_code = models.CharField(max_length=1000,blank=True)
	profile_pic = models.ImageField(blank=True)
	detail_address = models.TextField(blank=True)
	profile_status = models.BooleanField(default=False)
	lattitude = models.CharField(max_length=5000,blank=True)
	longitude = models.CharField(max_length=5000,blank=True)
	created_at = models.DateTimeField(auto_now_add=True,blank=True)
	updated_at = models.DateTimeField(auto_now=True,blank=True)

	def save(self, *args, **kwargs):
		self.user_conatct = self.user_conatct.lower()
		self.country = self.country.lower()
		self.state = self.state.lower()
		self.city = self.city.lower()
		self.detail_address = self.detail_address.lower()
		return super(UserProfile, self).save(*args, **kwargs)
	
	def __str__(self):
		return str(self.user)

class BussinessProfile(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)
	bussiness_name = models.CharField(max_length=1000,blank=True)
	bussiness_conatct = models.CharField(max_length=1000,blank=True)
	bussiness_email = models.EmailField(max_length=1000,blank=True)
	country = models.CharField(max_length=1000,blank=True)
	state = models.CharField(max_length=1000,blank=True)
	city = models.CharField(max_length=1000,blank=True)
	zip_code = models.CharField(max_length=1000,blank=True)
	detail_address = models.TextField(blank=True)
	lattitude = models.CharField(max_length=5000,blank=True)
	longitude = models.CharField(max_length=5000,blank=True)
	created_at = models.DateTimeField(auto_now_add=True,blank=True)
	updated_at = models.DateTimeField(auto_now=True,blank=True)
	def __str__(self):
		return self.bussiness_name


class PasswordChanged(models.Model):
	user = models.ForeignKey(User,on_delete=models.PROTECT,null=True, blank=True)
	temporary_otp = models.CharField(max_length=1000,blank=True)
	status = models.BooleanField(default=False,blank=True)
	created_at = models.DateTimeField(auto_now_add=True,blank=True)
	updated_at = models.DateTimeField(auto_now=True,blank=True)
	
	def __str__(self):
		return str(self.user)