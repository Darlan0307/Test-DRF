from rest_framework import viewsets, filters
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.pagination import PageNumberPagination

class CustomerPagination(PageNumberPagination):
    page_size = 10

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    pagination_class = CustomerPagination

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'cpf_cnpj', 'email']
    ordering_fields = ['name', 'qtd_seller']

