from django.contrib.admin import site
from .admin import CRUDAdmin
from crud.models import CRUD

site.register(CRUD, CRUDAdmin)
