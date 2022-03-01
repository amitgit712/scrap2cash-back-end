from django.contrib import admin
from django.urls import path,include
# from rest_framework_simplejwt import views as jwt_views
from django.conf import settings
from django.conf.urls.static import static
from b2c.views import CreatePostViewSet
from rest_framework import routers
router = routers.DefaultRouter()
router.register('create_post_api',CreatePostViewSet)


urlpatterns = [
    path('scrap2cashadmin/', admin.site.urls),
    path('',include('rest_auth.urls')), 
    path('',include(router.urls)),
    path('',include('b2c.urls')),
    path('',include('b2c.adds.urls')),
    path('',include('b2c.search.urls')),
    path('admin_dashboard/',include('admin_dashboard.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root= settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
    								