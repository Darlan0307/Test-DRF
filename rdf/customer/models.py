from django.db import models

class Customer(models.Model):
    name = models.CharField('nome', max_length=255)
    cpf_cnpj = models.CharField('CPF/CNPJ', max_length=18, unique=True)
    email = models.EmailField('e-mail', blank=True, null=True)
    is_blocked = models.BooleanField('bloqueado', default=False)
    qtd_seller = models.PositiveIntegerField('qtd. de vendedores', default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} ({self.cpf_cnpj})'
