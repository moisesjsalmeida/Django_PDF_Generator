from django.shortcuts import render
from .models import Text, Author
from .utils import render_pdf

# Visualizar os dados em uma página HTML
def index(request):
    texts = Text.objects.all()

    context = {
        'texts': texts,
    }

    return render(request, 'pdf.html', context)

# Gerar um pdf utilizando os dados e nossa função para renderizar html para pdf
def download_pdf(request):
	texts = Text.objects.all()

	context = {
		'texts': texts,
	}

	return render_pdf.render_pdf("pdf.html", context)






