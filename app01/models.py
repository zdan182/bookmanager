from django.db import models


# Create your models here.
class Publisher(models.Model):
    name = models.CharField(max_length=64)


class Book(models.Model):
    name = models.CharField(max_length=64)
    publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE)


class Author(models.Model):
    name = models.CharField(max_length=64)
    books = models.ManyToManyField('Book')
