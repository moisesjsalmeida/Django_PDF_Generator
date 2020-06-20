from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField

class Author(models.Model):

    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Author_detail", kwargs={"pk": self.pk})



class Text(models.Model): 

    title = models.CharField(max_length=100)
    text = RichTextField(max_length=10000)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Text"
        verbose_name_plural = "Texts"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Text_detail", kwargs={"pk": self.pk})
