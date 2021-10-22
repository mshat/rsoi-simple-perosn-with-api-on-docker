from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    address = models.CharField(max_length=300)
    work = models.CharField(max_length=200)

    def __str__(self):
        return self.name
