from django.contrib import admin
from django.urls import path
from testpdf.views import index, download_pdf

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('download_pdf', download_pdf),
]
