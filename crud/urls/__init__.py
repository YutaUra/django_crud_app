from django.urls import path
from crud import views as v

urlpatterns = [
    path('create/', v.CRUDUpdateView.as_view(), name='create'),
    path('detail/<pk>/', v.CRUDDetailView.as_view(), name='detail'),
    path('list/', v.CRUDListView.as_view(), name='list'),
    path('update/<pk>/', v.CRUDUpdateView.as_view(), name='update'),
    path('delete/<pk>/', v.CRUDDeleteView.as_view(), name='delete'),
]
