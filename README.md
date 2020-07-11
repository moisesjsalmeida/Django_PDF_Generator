# Django_PDF_Generator

![Django_PDF_Generator](https://github.com/moisesjsalmeida/Django_PDF_Generator/blob/master/project-logo.svg)

Este projeto foi um teste de geração de PDF, utilizando o [xhtml2pdf](https://github.com/xhtml2pdf/xhtml2pdf). 

Neste teste, utilizamos um modelo simples de texto de blog e autor. Para edição dos textos no `/admin`, utilizamos o [CKEditor](https://github.com/django-ckeditor/django-ckeditor).

Para facilitar o desenvolvimento, optei por separar a renderização em pdf em outra função. Assim, posso reutilizar em outras views ou mesmo em outros apps.


## utils/render_pdf
```python
render_pdf(template_path, context)
```

Esta funcionalidade permite a criação de pdfs através de um simples template HTML.

### Uso:

Em sua view, você deve importar a função:

```python
from .utils import render_pdf
```

A função já retorna uma resposta HTTP, então basta que sua view retorne o resultado da função.

```python
return render_pdf.render_pdf('nome_do_template_que_quero_renderizar.html', context)
```

### Parâmetros da função:

- template_path: caminho para o template que irá gerar o pdf
- context: objeto `context` que é gerado na view

### Criação de templates

Para facilitar a criação de pdfs, existe um template base, com configuração de página, cabeçalho, rodapé e configuração de fontes.

Então, o template que você quiser renderizar deve extendê-lo e carregar os estáticos.

```python 
{% extends 'pdf_base.html' %}
{% load static %}
```

Além disso, o `pdf_base.html` permite estilização com a utilização do `{% block styles %}`.

O conteúdo de seu pdf deve ir dentro do `{% block content %}`

### Limitações

Ao menos na versão do xhtml2pdf utilizada para este teste (0.2.4), a estilização utilizando um arquivo `.css` externo não tem funcionado. Daí a utilização do `{% block styles %}`. Além disso, a documentação já nos informa das limitações dos estilos que podemos utilizar. Algumas coisas podem dar mais trabalho, uma vez que teremos que realizar marcações à moda antiga: O Css grid ou flexbox não vão funcionar, teremos que organizar nossos itens através de uma table.
