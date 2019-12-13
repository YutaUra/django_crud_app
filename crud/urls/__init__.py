from django.urls import path
from crud import views as v

urlpatterns = [
    path('create/', v.CRUDCreateView.as_view(), name='create'),
]
