import os
from django.conf import settings
from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse
from .models import Text, Author
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

# Visualize data in HTML page
def index(request):
    texts = Text.objects.all()

    context = {
        'texts': texts,
    }

    return render(request, 'pdf.html', context)


# https://xhtml2pdf.readthedocs.io/en/latest/usage.html
# This function converts relative URLs to absolute system paths
def link_callback(uri, rel):
	"""
	Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
	"""
	# Por algum motivo maluco, o finders.find não encontra o arquivo se estiver com o caminho /static/
	uri = uri.replace("/static/", "")
	result = finders.find(uri)
	searched_locations = finders.searched_locations
	if result:
		if not isinstance(result, (list, tuple)):
			result = [result]
		result = list(os.path.realpath(path) for path in result)
		path=result[0]
	else:
		sUrl = settings.STATIC_URL
		sRoot = settings.STATIC_ROOT
		mUrl = settings.MEDIA_URL   
		mRoot = settings.MEDIA_ROOT

		if uri.startswith(mUrl):
			path = os.path.join(mRoot, uri.replace(mUrl, ""))
		elif uri.startswith(sUrl):
			path = os.path.join(sRoot, uri.replace(sUrl, ""))
		else:
			return uri

	# make sure that file exists
	if not os.path.isfile(path):
		raise Exception(
			'media URI must start with %s or %s' % (sUrl, mUrl)
		)
	print("--------------------------")
	print("este é o path: " + path)
	print("--------------------------")
	return path

# This view generates a pdf file from the template
def render_pdf_from_html(request):
    # Getting the template
    template_path = 'pdf.html'
    template = get_template(template_path)

    # Getting all objects and build context to pass to dinamic HTML
    texts = Text.objects.all()

    context = {
        'texts': texts,
    }

    html_to_render = template.render(context)
    
    # A response with content-type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="my_pdf.pdf"'

    # Create the pdf
    pisa_status = pisa.CreatePDF(html_to_render, dest=response, link_callback=link_callback)

    # If error, show the source
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html_to_render + '</pre>')
    
    return response





