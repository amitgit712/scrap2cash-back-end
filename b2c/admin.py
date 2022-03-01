from django.contrib import admin
from b2c.models import(
	CreateIndustrialPost,
	IndustrialPostImages,
	EnquiryMail,ScrapPrice
	)

# admin.site.register(CreateGeneralPost)
admin.site.register(CreateIndustrialPost)
# admin.site.register(GeneralPostImages)
admin.site.register(IndustrialPostImages)
admin.site.register(EnquiryMail)
admin.site.register(ScrapPrice)
