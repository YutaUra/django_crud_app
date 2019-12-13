from django.views.generic import ListView
from crud.models import CRUD


class CRUDListView(ListView):
    model = CRUD
    template_name = 'crud/list.html'
