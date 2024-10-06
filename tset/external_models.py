# external_app/models.py

from django.db import models

class ExternalData(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        managed = False  # Prevents Django from trying to create or modify this table
        db_table = 'external_table'  # Use the name of the table in the external database