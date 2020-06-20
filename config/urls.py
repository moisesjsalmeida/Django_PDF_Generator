from django.contrib import admin
from django.urls import path
from testpdf.views import index, render_pdf_from_html

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('render_pdf_from_html', render_pdf_from_html),
]
