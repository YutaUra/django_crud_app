from django.views.generic import DetailView
from crud.models import CRUD


class CRUDDetailView(DetailView):
    model = CRUD
    template_name = 'crud/detail.html'
