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

    def __str__(self):
        return f'{self.name}'


class Veggie(models.Model):
    name = models.CharField(max_length=30)
    family = models.ForeignKey(VeggieFamily, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

class Company(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return f'{self.name}'

class Month(models.Model):
    name = models.CharField(max_length=20)
    order = models.IntegerField(unique=True)


class SunScale(models.Model):
    name = models.CharField(max_length=20)


class WaterScale(models.Model):
    name = models.CharField(max_length=20)


class SoilScale(models.Model):
    name = models.CharField(max_length=20)


class Seed(models.Model):
    veggie = models.ForeignKey(Veggie, on_delete=models.CASCADE)
    variety = models.CharField(max_length=50)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    comment = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class GrowVeggie(models.Model):
    veggie = models.ForeignKey(Veggie, on_delete=models.CASCADE)
    sun = models.ManyToManyField(SunScale)
    water = models.ManyToManyField(WaterScale)
    soil = models.ManyToManyField(SoilScale)
    sow = models.ManyToManyField(Month)
    comment = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Plan(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Bed(models.Model):
    name = models.CharField(max_length=50)
    sun = models.ForeignKey(SunScale, on_delete=models.CASCADE)
    water = models.ForeignKey(WaterScale, on_delete=models.CASCADE)
    soil = models.ForeignKey(SoilScale, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class VeggieBed(models.Model):
    veggie = models.ForeignKey(Veggie, on_delete=models.CASCADE)
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE)
    progress = models.IntegerField(choices=PROGRESS)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

