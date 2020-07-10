import os
from django.conf import settings
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


# https://xhtml2pdf.readthedocs.io/en/latest/usage.html
# Esta função converte URLs em caminhos de sistema. 
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
		path = result[0]
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

	return path


# Esta função retorna uma resposta http contendo o pdf
def render_pdf(template_path, context):
    template = get_template(template_path)

    html_to_render = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="my_pdf.pdf"'

    # Criando o pdf
    pisa_status = pisa.CreatePDF(
    	html_to_render, dest=response, link_callback=link_callback)

    # Em caso de erro, retornar o source code
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html_to_render + '</pre>')

    return response
