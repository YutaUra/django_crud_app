from django.urls import reverse
from django.views.generic import UpdateView
from crud.forms import CRUDForm
from crud.models import CRUD


class CRUDUpdateView(UpdateView):
    model = CRUD
    form_class = CRUDForm
    template_name = 'crud/update.html'

    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.object.id})
