from django.views import View
from rest_framework import viewsets, filters
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

class CustomerPagination(PageNumberPagination):
    page_size = 10

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    pagination_class = CustomerPagination

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'cpf_cnpj', 'email']
    ordering_fields = ['name', 'qtd_seller']

class CustomerListTemplateView(TemplateView):
    template_name = 'customers/list.html'

class CustomerFormView(View):
    def get(self, request, pk=None):
        customer = None
        if pk:
            customer = get_object_or_404(Customer, pk=pk)
        return render(request, 'customers/form.html', {'customer': customer or {}})

class CustomerDeleteView(View):
    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        return render(request, 'customers/confirm_delete.html', {'customer': customer})
