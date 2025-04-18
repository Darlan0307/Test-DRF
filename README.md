## Criando sistema com Django Rest Framework (DRF)

### 1. Criar e ativar ambiente virtual

```bash
  python3.12 -m venv venv
  source venv/bin/activate  # Linux / macOS
  venv\Scripts\activate   # Windows
```

### 2. Instalando dependências

```bash
  pip install django djangorestframework
```

### 3. Criando o projeto

```bash
  django-admin startproject myproject
  cd myproject
```

### 4. Criando o primeiro App

```bash
  python manage.py startapp name_app
```

### 5. Ajustando o arquivo settings.py

```py
  INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Add Django Rest Framework
    'name_app',  # Add your app
]
```

<details>
  <summary>Criando o primeiro endpoint</summary>
  <br/>
  
  - Criar os primeiros models

```py
from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return self.name
```

- Rodando as migrations

```bash
  python manage.py makemigrations
  python manage.py migrate
```

- Criando o Serializer

```py
  from rest_framework import serializers
  from .models import Item

  class ItemSerializer(serializers.ModelSerializer):
      class Meta:
          model = Item
          fields = '__all__'
```

- Criando a View

```py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Item
from .serializers import ItemSerializer


class ItemsView(APIView):
    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
```

- Configurando a URL do app

```py
  from django.urls import path
from .views import ItemsView


urlpatterns = [
    path('items/', ItemsView.as_view(), name='items'),
]
```

- Configurando a URL da api

```py
 from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Add this line
]
```

</details>

### 6. Habilitando a UI do DRF no navegador

Adicionar no arquivo settings.py

```py
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}
```

### 7. Rodando o servidor

```bash
  python manage.py runserver
```
