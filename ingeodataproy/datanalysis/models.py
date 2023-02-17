from django.db import models


# Create your models here.
class GasPrices(models.Model):
    date = models.DateField()
    a1 = models.FloatField()
    a2 = models.FloatField()
    a3 = models.FloatField()
    r1 = models.FloatField()
    r2 = models.FloatField()
    r3 = models.FloatField()
    m1 = models.FloatField()
    m2 = models.FloatField()
    m3 = models.FloatField()
    p1 = models.FloatField()
    p2 = models.FloatField()
    p3 = models.FloatField()
    d1 = models.FloatField()