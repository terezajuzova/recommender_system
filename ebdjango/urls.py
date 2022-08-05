from django.contrib import admin
from django.urls import include, path

# Import view

from ebdjango import views

urlpatterns = [

     path('ebdjango/', include('ebdjango.urls')),

     path('admin/', admin.site.urls)

]