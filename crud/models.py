from django.db import models


class CRUD(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
