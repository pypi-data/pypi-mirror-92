from django.contrib import admin
import uuid

import logging

from django.db import models
from django.forms import model_to_dict
from django.db.models import EmailField, ForeignKey, DO_NOTHING, OneToOneField, ManyToManyField

logger = logging.getLogger('base')


class unBaseAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'


class unBaseInline(admin.TabularInline):
    can_delete = False
    extra = 0
    editable_fields = []
    actions = None

    def get_readonly_fields(self, request, obj=None):
        return self.fields or [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request, obj):
        return False



class unBaseModel(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False, null=False)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        get_latest_by = 'created_at'

    def dict(self):
        d = model_to_dict(self)
        for k in d:
            if isinstance(d[k], list) and d[k] and isinstance(d[k][0], models.Model):
                d[k] = list(map(model_to_dict, d[k]))
        return d

    def __str__(self):
        return "{} {}".format(str(self._meta), self.id)




def generate_short_code(prefix, size):
    import secrets, string
    return prefix + ''.join([secrets.choice(string.ascii_uppercase + string.digits) for _ in range(size)])


class LowerCaseEmailField(EmailField):
    def get_prep_value(self, value):
        return (super().get_prep_value(value) or "").lower()


class LooseForeignKey(ForeignKey):

    def __init__(self, to, **kwargs):
        kwargs['on_delete'] = DO_NOTHING
        kwargs['db_constraint'] = False

        super().__init__(to,
                         **kwargs)

class LooseOneToOneField(OneToOneField):
    def __init__(self, to, **kwargs):
        kwargs['unique'] = True
        kwargs['on_delete'] = DO_NOTHING
        kwargs['db_constraint'] = False

        super().__init__(to,
                         **kwargs)


class LooseManyToManyField(ManyToManyField):
    def __init__(self, to, **kwargs):
        kwargs['db_constraint'] = False

        super().__init__(to,
                         **kwargs)