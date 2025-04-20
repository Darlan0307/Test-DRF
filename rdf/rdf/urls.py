from django.urls import path
from .views import ItemsView, ItemDetailView


app_name = 'rdf'

urlpatterns = [
    path('items/', ItemsView.as_view(), name='item-list'),
     path('items/<int:pk>/', ItemDetailView.as_view(), name='item-detail')
]