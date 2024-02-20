from django.db import models

# Create your models here.


class Par(models.Model):
    name = models.CharField(max_length=100)
    #lastName = models.CharField(max_length=100)
    armNum = models.IntegerField()
    swimTime = models.DurationField(null=True, blank=True)
    rsrTime = models.DurationField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True) # takes timestamp of when it was created/updated
    created = models.DateTimeField(auto_now_add=True)
    swimPts = models.IntegerField(null=True, blank=True)
    rsrPts = models.IntegerField(null=True, blank=True)
    rank = models.IntegerField(null=True, blank=True)
    totalPts = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.armNum)


