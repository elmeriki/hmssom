from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('hmmauth.urls')),
    path('', include('customer.urls')),
    path('', include('hospital.urls')),
    path('', include('administrator.urls')),
    path('', include('finance.urls')),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

