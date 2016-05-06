from django.db import models


class TestItemModel(models.Model):
    """ Item used for testing. """

    slug = models.SlugField()

    def __unicode__(self):
        return self.slug

    def get_absolute_url(self):
        return 'bogus'
