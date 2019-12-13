from django.forms import ModelForm

from crud.models import CRUD


class CRUDForm(ModelForm):
    class Meta:
        model = CRUD
        fields = ('name',)
