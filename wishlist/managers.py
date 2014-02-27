from django.db.models.query import QuerySet
from django.db.models import Manager


class UserQuerySet(QuerySet):
    """ Custom QuerySet for UserManager. """

    def for_user(self, user):
        """ Return items for a given user. """
        return self.filter(user=user)


class UserManager(Manager):
    """ Custom manager adding for_user(user) method. """

    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)

    def for_user(self, user):
        return self.get_queryset().for_user(user=user)
