from django.urls import path
from crud import views as v

urlpatterns = [
    path('create/', v.CRUDCreateView.as_view(), name='create'),
    path('detail/<pk>/', v.CRUDDetailView.as_view(), name='detail')
]
