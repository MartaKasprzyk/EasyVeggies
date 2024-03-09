from django.contrib.auth.models import User
from django.db import models

PROGRESS = {
    (1, "sown"),
    (2, "growing"),
    (3, "blooming"),
    (4, "bears fruit"),
    (5, "harvested"),
}


class VeggieFamily(models.Model):
    name = models.CharField(max_length=30)
    order = models.IntegerField()


class Veggie(models.Model):
    name = models.CharField(max_length=30)
    family = models.ForeignKey(VeggieFamily, on_delete=models.CASCADE)


class Company(models.Model):
    name = models.CharField(max_length=60)


class Month(models.Model):
    name = models.CharField(max_length=20)
    order = models.IntegerField(unique=True)


class Scale(models.Model):
    name = models.CharField(max_length=20)


class Seed(models.Model):
    veggie = models.ForeignKey(Veggie, on_delete=models.CASCADE)
    variety = models.CharField(max_length=50)
    family = models.ForeignKey(VeggieFamily, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    comment = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class GrowVeggie(models.Model):
    veggie = models.ForeignKey(Veggie, on_delete=models.CASCADE)
    sun = models.ManyToManyField(Scale, related_name='sun')
    water = models.ManyToManyField(Scale, related_name='water')
    soil = models.ManyToManyField(Scale, related_name='soil')
    sow = models.ManyToManyField(Month, related_name='sow')
    harvest = models.ManyToManyField(Month, related_name='harvest')
    comment = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Plan(models.Model):
    name = models.CharField(max_length=50)
    bed = models.IntegerField()
    veggie_family = models.ForeignKey(VeggieFamily, on_delete=models.CASCADE)
    veggies = models.ManyToManyField(Veggie)
    progress = models.IntegerField(choices=PROGRESS)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
