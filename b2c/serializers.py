from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from b2c.models import CreateIndustrialPost,IndustrialPostImages
from admin_dashboard.models import (
	BussinessType,Category,
	Subcategory,ProductType
	) 

class BussinessTypeSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = BussinessType
		fields = ('id',)

class ProductTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductType
		fields = ('id',)


class CreateIndustrialPostSerializer(serializers.HyperlinkedModelSerializer):	
	class Meta:
		model = CreateIndustrialPost
		fields =(
			"bussiness_type_id","product_type_id","material_id","sub_material_id",
			"category_id_id","sub_category_id_id",
			"shape_id","length","width","thickness","quantity","weight",
			"ids","dimeter","product_description","bargening","selling_price",
			"user_remove_post","suspended","admin_approval","created_at",
			"updated_at",
			)



class IndustrialPostImagesSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		models = IndustrialPostImages
		fields = ['url','industry_post','images']
