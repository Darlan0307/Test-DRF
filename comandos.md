## Criar e ativar virtualenv

```bash
 python3.13 -m venv env
 source env/bin/activate
```

## Sair do virtualenv

```bash
 deactivate
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

## atualizando model especifico

```bash
 python manage.py makemigrations name_model
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

 python manage.py test e2e_tests/
```

## apagando banco de dados

```bash
 rm db.sqlite3
 find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
 find . -path "*/migrations/*.pyc"  -delete
```
