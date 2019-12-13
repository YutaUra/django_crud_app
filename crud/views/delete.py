from django.urls import reverse
from django.views.generic import DeleteView
from crud.forms import CRUDForm
from crud.models import CRUD


class CRUDDeleteView(DeleteView):
    model = CRUD
    template_name = 'crud/delete.html'

    def get_success_url(self):
        return reverse('list')
