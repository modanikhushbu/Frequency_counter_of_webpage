from django.db import models
from jsonfield import JSONField

class url_data(models.Model):
    url = models.URLField()
    result = JSONField()

    def __str__(self):
        return self.url