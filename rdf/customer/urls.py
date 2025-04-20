# from django.urls import path
# from .views import CustomerViewSet


# app_name = 'customer'

# urlpatterns = [
#     path('', CustomerViewSet.as_view({'get': 'list', 'post': 'create'}), name='crud-customer'),
# ]


from django.urls import include, path
from rest_framework import routers
from .views import CustomerViewSet

router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')

urlpatterns = [
    path('', include(router.urls)),
]
