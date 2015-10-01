from django.db import models

# Remember: fat models, skinny views.
# And remember to register your models in admin.

class PghBoard(models.Model):
    name = models.CharField(max_length=255)
    history = models.TextField(null=True, blank=True)
    contact = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    creation_date = models.DateField(null=True, blank=True)
    meeting_place = models.CharField(max_length=255, null=True, blank=True)
    meeting_time = models.CharField(max_length=100, null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    link = models.URLField(max_length=255, null=True, blank=True)


class PghBoardMember(models.Model):
    name_first = models.CharField(max_length=40)
    name_last = models.CharField(max_length=40)
    term_expires = models.DateField()
    board = models.ManyToManyField(PghBoard)

