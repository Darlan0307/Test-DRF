from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Item
from .serializers import ItemSerializer

class ItemAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.item1 = Item.objects.create(name="Item 1", description="Descrição do Item 1")
        self.item2 = Item.objects.create(name="Item 2", description="Descrição do Item 2")
        self.list_url = reverse('rdf:item-list')
        
    def test_get_all_items(self):
        """Teste para verificar se conseguimos obter a lista de todos os itens"""
        response = self.client.get(self.list_url)
        
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 2)
    
    def test_create_item(self):
        """Teste para verificar se conseguimos criar um novo item"""
        data = {
            "name": "Novo Item",
            "description": "Descrição do Novo Item"
        }
        
        response = self.client.post(self.list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 3)
    
    def test_get_single_item(self):
        """Teste para verificar se conseguimos obter um único item"""
        detail_url = reverse('rdf:item-detail', args=[self.item1.id])
        response = self.client.get(detail_url)
        
        serializer = ItemSerializer(self.item1)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
    
    def test_update_item(self):
        """Teste para verificar se conseguimos atualizar um item"""
        detail_url = reverse('rdf:item-detail', args=[self.item1.id])
        updated_data = {
            "name": "Item 1 Atualizado",
            "description": "Nova descrição"
        }
        
        response = self.client.put(detail_url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item1.refresh_from_db()
        self.assertEqual(self.item1.name, "Item 1 Atualizado")
    
    def test_partial_update_item(self):
        """Teste para verificar se conseguimos atualizar parcialmente um item"""
        detail_url = reverse('rdf:item-detail', args=[self.item1.id])
        partial_data = {
            "description": "Nova descrição"
        }
        
        response = self.client.patch(detail_url, partial_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item1.refresh_from_db()
        self.assertEqual(self.item1.name, "Item 1") 
        self.assertEqual(self.item1.description, 'Nova descrição')
    
    def test_delete_item(self):
        """Teste para verificar se conseguimos deletar um item"""
        detail_url = reverse('rdf:item-detail', args=[self.item1.id])
        response = self.client.delete(detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 1)
        
    def test_get_nonexistent_item(self):
        """Teste para verificar o comportamento ao tentar obter um item que não existe"""
        non_existent_id = 999
        detail_url = reverse('rdf:item-detail', args=[non_existent_id])
        response = self.client.get(detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)