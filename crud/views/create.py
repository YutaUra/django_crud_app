from django.views.generic import CreateView
from crud.forms import CRUDForm
from crud.models import CRUD


class CRUDCreateView(CreateView):
    model = CRUD
    form_class = CRUDForm
    template_name = 'crud/create.html'
