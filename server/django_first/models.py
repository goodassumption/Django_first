from django.db import models

class FirstModel(models.Model):
    date = models.DateField()
    # integrer = models.IntegrerField()
    string = models.CharField(max_length = 100)
