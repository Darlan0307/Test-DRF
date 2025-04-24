# from django.urls import path
# from .views import CustomerViewSet


# app_name = 'customer'

# urlpatterns = [
#     path('', CustomerViewSet.as_view({'get': 'list', 'post': 'create'}), name='crud-customer'),
# ]


from django.urls import include, path
from rest_framework import routers
from .views import CustomerViewSet, CustomerListTemplateView,CustomerFormView, CustomerDeleteView


router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')

urlpatterns = [
    path('', include(router.urls)),
    path('clientes/', CustomerListTemplateView.as_view(), name='list-customers'),
    path('clientes/novo/', CustomerFormView.as_view(), name='customer_create'),
    path('clientes/<int:pk>/editar/', CustomerFormView.as_view(), name='customer_edit'),
    path('clientes/<int:pk>/excluir/', CustomerDeleteView.as_view(), name='customer_delete'),
]
