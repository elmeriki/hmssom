from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static 

admin.site.site_header="Hmssom"
admin.site.site_title ="Hmssom Admin Portal"
admin.site.index_title="Welcome to Hmssom"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('hmmauth.urls')),
    path('', include('customer.urls')),
    path('', include('hospital.urls')),
    path('', include('administrator.urls')),
    path('', include('finance.urls')),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

