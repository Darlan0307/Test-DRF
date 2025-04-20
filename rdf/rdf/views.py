from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Item
from .serializers import ItemSerializer

class ItemsView(APIView):
    """
    View para listar todos os itens ou criar um novo item.
    """
    def get(self, request):
        """Lista todos os itens"""
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Cria um novo item"""
        serializer = ItemSerializer(data=request.data)
        
        if serializer.is_valid():
            external_id = serializer.validated_data.get('external_id')

            if external_id and Item.objects.filter(external_id=external_id).exists():
                return Response({"message": "Item já existe"}, status=status.HTTP_409_CONFLICT)
        
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemDetailView(APIView):
    """
    View para recuperar, atualizar ou deletar um item específico.
    """
    def get_object(self, pk):
        """Helper method para obter o objeto com o pk fornecido"""
        try:
            return Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """Recupera um item específico"""
        item = self.get_object(pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk):
        """Atualiza um item específico"""
        item = self.get_object(pk)
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """Atualiza parcialmente um item específico"""
        item = self.get_object(pk)
        serializer = ItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Deleta um item específico"""
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)