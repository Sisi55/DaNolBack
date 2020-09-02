from django.urls import path
from . import views

urlpatterns = [
    # /sheets/
    # path('test/', views.test_api),
    path('save/archiving/', views.save_archiving_data),  # 아카이빙 데이터 저장 : 재사용 안하는 api
    path('contents/', views.get_contents),
]
