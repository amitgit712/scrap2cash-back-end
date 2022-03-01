from django.contrib import admin
from admin_dashboard.models import (
	BussinessType,Category,
	Subcategory,ProductType,
	Material,Sub_material,
	Shape,Units
	)
admin.site.register(BussinessType)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(ProductType)
admin.site.register(Material)
admin.site.register(Sub_material)
admin.site.register(Shape)
admin.site.register(Units)

# admin.site.register(FieldsLable)
