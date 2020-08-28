from django.urls import path
from . import views

urlpatterns = [
    # /sheets/
    # path('test/', views.test_api),
    path('test/', views.test_excel_api), #
]
