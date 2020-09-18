from django.urls import path
from . import views

urlpatterns = [
    # /sheets/
    # path('test/', views.test_api),
    path('save/archiving/', views.save_archiving_data),  # 아카이빙 데이터 저장 : 재사용 안하는 api
    # 후원기업 저장 api
    path('save/sponsor/', views.save_sponsor_data),  # ?size=&apiKey=
    path('save/committee/', views.save_committee_data),
    path('save/content2020/', views.save_content2020_data),

    # 발표자로 아카이빙 & 2020 타임 테이블
    path('contents/', views.get_contents),
    path('sponsors/', views.get_sponsors),
    path('committee-members/', views.get_members),
    # content 2020 이 아직 트랙 미완이라 쭉 가져만 오기
    path('contents-2020/', views.get_contents_2020_TMP),
    path('presenters-2020/', views.get_presenters_2020_TMP),
]
