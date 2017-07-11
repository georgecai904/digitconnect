from django.db import models

# Create your models here.


class Breadcrumb(models.Model):
    name = models.CharField(max_length=20)
    url_name = models.CharField(max_length=20)
    parent = models.ForeignKey("core.Breadcrumb", default=None, null=True)
    class_name = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.name

    def get_list(self):
        _list = [[self.name, '', self.class_name, '']]
        current = self
        while current.parent:
            current = current.parent
            _list = [[current.name, current.url_name, current.class_name, '']] + _list
        return _list