from django.db import models

# Create your models here.
class ShortLink(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    link = models.URLField()
    created_date = models.DateTimeField(auto_now_add=True)
    visited_counter = models.PositiveIntegerField()
