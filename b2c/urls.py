from b2c.views import(
	send_form_attributes,#create_general_post,
	get_category,get_subcategory,get_producttype,
	get_formdata,#add_seller_info,
	create_post,upload_files,home_data,
	recent_post,post_detail_view,mail_product_requirements,
	category_wise,all_category,all_subcategory,get_material,
	get_submaterial,get_shape,get_post_data,update_post,update_files,get_unit,scrapdata
	)
from django.urls import path

app_name ="b2c"

urlpatterns = [
	path('send_form_attributes/',send_form_attributes,name="send_form_attributes"),
	path('get_category/<BussinessTypeId>/',get_category,name="get_category"),
	path('get_subcategory/<categoryId>/',get_subcategory,name="get_subcategory"),
	path('get_producttype/',get_producttype,name="get_producttype"),
	path('get_material/',get_material,name="get_material"),
	path('get_shape/',get_shape,name="get_shape"),
	path('get_submaterial/<materialId>/',get_submaterial,name="get_submaterial"),
	path('get_formdata/<BussinessTypeId>/',get_formdata,name="get_formdata"),
	path('create_post/',create_post,name="create_post"),
	path('upload_files/',upload_files,name="upload_files"),
	path('home_data/',home_data,name="home_data"),
	path('recent_post/',recent_post,name="recent_post"),
	path('post_detail/<postId>/',post_detail_view,name="post_detail"),
	path('mail_product_requirements/<postId>/',mail_product_requirements,name="mail_product_requirements"),
	path('category_wise/<catId>/',category_wise,name="category_wise"),
	path('all_category/',all_category,name="all_category"),
	path('all_subcategory/',all_subcategory,name="all_subcategory"),
	path('get-post-data/<id>/',get_post_data,name="get_post_data"),
	path('update-post/<id>/',update_post,name="update_post"),
	path('update_files/<id>/',update_files,name="update_files"),
	path('get_unit/',get_unit, name="get_unit"),
	path('scrapdata/',scrapdata,name="scrapdata"),
]
