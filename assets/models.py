from django.contrib.gis.db import models

# Create your models here.


class Institution(models.Model):
    """
        institution model fields
    """
    name = models.CharField(db_index=True, max_length=255, unique=True)
    location = models.PointField(srid=4326, null=True, geography=True)

    def __str__(self):
        return self.name


class Head(models.Model):
    institution = models.ForeignKey(
        Institution, on_delete=models.CASCADE, related_name="institution_head")
    name = models.CharField(db_index=True, max_length=255, unique=False)
    contact = models.IntegerField(db_index=True, unique=False)

    def __str__(self):
        return self.name


class Report(models.Model):

    institution = models.ForeignKey(
        Institution, on_delete=models.CASCADE, related_name="institution_report")
    name = models.CharField(db_index=True, max_length=255, unique=False)
    description = models.CharField(db_index=True, max_length=255, unique=False)
    report = models.FileField(
        blank=False, default='/media/Ramani_GEO.pdf', null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
