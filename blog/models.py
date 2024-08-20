from django.db import models


class Author(models.Model):
    full_name = models.CharField(max_length=50)
    pen_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.full_name} (a.k.a. {self.pen_name})"


class Article(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=250)
    content = models.TextField()
    created_on = models.DateField(auto_now_add=True)
    modified_on = models.DateField(auto_now=True)
    author = models.ForeignKey(Author)

    def __str__(self):
        return f"{self.title}\n{self.description}\n\
                last modified: {self.modified_on}"
