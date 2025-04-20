from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Customer


class BaseCustomerTestCase(TestCase):
    """Classe base para testes de clientes"""
    def setUp(self):
        self.client = APIClient()
        
        self.customer1 = Customer.objects.create(
            name="Cliente 1", 
            cpf_cnpj="12345678901",
            email="cliente1@teste.com"
        )
        self.customer2 = Customer.objects.create(
            name="Cliente 2", 
            cpf_cnpj="98765432101",
            email="cliente2@teste.com",
            is_blocked=True,
            qtd_seller=5
        )
        
        self.list_url = reverse('customer-list')


class CustomerListTestCase(BaseCustomerTestCase):
    """Testes para operações de listagem de clientes"""
    
    def test_get_all_customers(self):
        """Teste para verificar se conseguimos obter a lista de todos os clientes"""
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 2)


class CustomerCreateTestCase(BaseCustomerTestCase):
    """Testes para operações de criação de clientes"""
    
    def test_create_customer(self):
        """Teste para verificar se conseguimos criar um novo cliente"""
        data = {
            "name": "Novo Cliente",
            "cpf_cnpj": "11122233344",
            "email": "novocliente@teste.com"
        }
        
        response = self.client.post(self.list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 3)
        self.assertEqual(response.data['name'], "Novo Cliente")
    
    def test_create_invalid_customer(self):
        """Teste para verificar validação ao criar cliente sem campos obrigatórios"""
        data = {
            "email": "invalido@teste.com"
        }
        
        response = self.client.post(self.list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Customer.objects.count(), 2)
    
    def test_error_validation(self):
        """Teste para verificar erros de validação"""
        data = {
            "name": "Cliente 1",
            "cpf_cnpj": "12345678901",
            "email": "cliente1@teste.com",
            "is_blocked": True,
            "qtd_seller": 10
        }
        
        response = self.client.post(self.list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Customer.objects.count(), 2)


class CustomerDetailTestCase(BaseCustomerTestCase):
    """Testes para operações em clientes específicos (detalhe, atualização, exclusão)"""
    
    def test_get_single_customer(self):
        """Teste para verificar se conseguimos obter um único cliente"""
        detail_url = reverse('customer-detail', args=[self.customer1.id])
        response = self.client.get(detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.customer1.name)
        self.assertEqual(response.data['cpf_cnpj'], self.customer1.cpf_cnpj)
    
    def test_update_customer(self):
        """Teste para verificar se conseguimos atualizar um cliente"""
        detail_url = reverse('customer-detail', args=[self.customer1.id])
        updated_data = {
            "name": "Cliente 1 Atualizado",
            "cpf_cnpj": "12345678901",
            "email": "atualizado@teste.com"
        }
        
        response = self.client.put(detail_url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.customer1.refresh_from_db()
        self.assertEqual(self.customer1.name, "Cliente 1 Atualizado")
        self.assertEqual(self.customer1.email, "atualizado@teste.com")
    
    def test_partial_update_customer(self):
        """Teste para verificar se conseguimos atualizar parcialmente um cliente"""
        detail_url = reverse('customer-detail', args=[self.customer1.id])
        partial_data = {
            "is_blocked": True
        }
        
        response = self.client.patch(detail_url, partial_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.customer1.refresh_from_db()
        self.assertEqual(self.customer1.name, "Cliente 1") 
        self.assertTrue(self.customer1.is_blocked)
    
    def test_delete_customer(self):
        """Teste para verificar se conseguimos deletar um cliente"""
        detail_url = reverse('customer-detail', args=[self.customer1.id])
        response = self.client.delete(detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Customer.objects.count(), 1)
    
    def test_get_nonexistent_customer(self):
        """Teste para verificar o comportamento ao tentar obter um cliente que não existe"""
        non_existent_id = 999
        detail_url = reverse('customer-detail', args=[non_existent_id])
        response = self.client.get(detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CustomerFilterSearchTestCase(BaseCustomerTestCase):
    """Testes para funcionalidades de busca e filtros"""
    
    def test_search_customer(self):
        """Teste para verificar a funcionalidade de busca"""
        search_url = f"{self.list_url}?search=Cliente 1"
        response = self.client.get(search_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['name'], "Cliente 1")
    
    def test_ordering_customer(self):
        """Teste para verificar a funcionalidade de ordenação"""
        # Testando ordenação ascendente
        ordering_url = f"{self.list_url}?ordering=qtd_seller"
        response = self.client.get(ordering_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # O primeiro cliente tem qtd_seller=0 (padrão) e o segundo tem qtd_seller=5
        self.assertEqual(response.data['results'][0]['name'], "Cliente 1")
        
        # Testando ordenação decrescente
        ordering_url = f"{self.list_url}?ordering=-qtd_seller"
        response = self.client.get(ordering_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['name'], "Cliente 2")


class CustomerPaginationTestCase(BaseCustomerTestCase):
    """Testes para funcionalidade de paginação"""
    
    def test_pagination(self):
        """Teste para verificar a funcionalidade de paginação"""
        # Criar mais clientes para testar a paginação
        for i in range(3, 13): 
            Customer.objects.create(
                name=f"Cliente {i}",
                cpf_cnpj=f"{i}{'0' * 10}",
                email=f"cliente{i}@teste.com"
            )
        
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10) 
        self.assertTrue(response.data['next'])
        
        # Testando a segunda página
        page_2_url = response.data['next']
        page_2_url = page_2_url.replace('http://testserver', '')
        response = self.client.get(page_2_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertIsNone(response.data['next'])