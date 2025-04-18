## Criar e ativar virtualenv

```bash
 python3.13 -m venv env
 source env/bin/activate
```

## Criar arquivo requirements.txt

```bash
 pip freeze > requirements.txt
```

## instalar dependências

```bash
 pip install -r requirements.txt
```

## criar banco de dados

```bash
 python manage.py makemigrations
 python manage.py migrate
```

## criar usuário

```bash
 python manage.py createsuperuser
```

python manage.py createsuperuser

## rodar servidor

```bash
 python manage.py runserver
```

## executar testes

```bash
 python manage.py test rdf
```

## apagando banco de dados

```bash
 rm db.sqlite3
 find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
 find . -path "*/migrations/*.pyc"  -delete
```
