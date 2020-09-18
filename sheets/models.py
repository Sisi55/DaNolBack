from django.db import models


class Member(models.Model):  # 발표자/준비위
    # Member: email, name, belongTo
    PreparatoryCommittee, Presenter = '준비위', '발표자'
    CHOICES = [
        (PreparatoryCommittee, '준비위'),
        (Presenter, '발표자'),
    ]
    kind = models.CharField(
        max_length=15,
        choices=CHOICES,
        default=Presenter,
        blank=True, null=True
    )

    email = models.CharField('이메일', max_length=30, null=True, default='')
    image_url = models.TextField('사진', null=True, default='', blank=True)
    name = models.CharField('이름', max_length=15, default='')
    introduction = models.TextField('소개글', null=True, default='', blank=True)
    # 소속: 발표자
    belongTo = models.CharField('소속', max_length=30, null=True, default='')


class SNS(models.Model):  # 발표자 sns 계정
    owner = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="sns", null=True)

    Twitter, GitHub, Facebook, Insta, Linkedin, Blog = '트위터', '깃허브', '페이스북', '인스타', '링크드인', '블로그'
    SNS_CHOICES = [
        (Twitter, '트위터'), (GitHub, '깃허브'), (Facebook, '페이스북'),
        (Insta, '인스타'), (Linkedin, '링크드인'), (Blog, '블로그'),
    ]
    kind = models.CharField(
        max_length=15,
        choices=SNS_CHOICES,
        blank=True, null=True, default=''
    )
    link = models.TextField('sns링크', default='')


# kind link

class Content(models.Model):  # 발표
    # Content: presenter, title, presentation_time, introduction, kind
    year = models.CharField('연도', max_length=5, default='2020')
    track_num = models.CharField('트랙번호', max_length=2, null=True, default='')
    order = models.CharField('발표순번', max_length=2, null=True, default='')
    presenter = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="contents", null=True)
    title = models.TextField('발표제목', default='', null=True, blank=True)
    source_link = models.TextField('자료링크', null=True, default='')

    presentation_time = models.CharField('발표시간', max_length=10, null=True, default='')  # ver 2020
    difficulty = models.CharField('발표 난이도', max_length=15, null=True, default='')  # ver 2020

    introduction = models.TextField('내용소개', null=True, default='', blank=True)

    GENERAL_SESSIONS, IGNITE_SESSIONS, COMMUNITY_COLLABORATION_SESSIONS = '일반 세션', '이그나이트', '커뮤니티 콜라보'
    SPONSOR_SPECIAL_SESSIONS, OUTSIDE_INVITATIONS_SESSIONS = '스폰서 특별 세션', '외부 초청'
    SESSION_CHOICES = [
        (GENERAL_SESSIONS, '일반 세션'), (IGNITE_SESSIONS, '이그나이트'),
        (SPONSOR_SPECIAL_SESSIONS, '스폰서 특별 세션'), (OUTSIDE_INVITATIONS_SESSIONS, '외부 초청'),
        (COMMUNITY_COLLABORATION_SESSIONS, '커뮤니티 콜라보'),
    ]
    kind = models.CharField(
        max_length=15,
        choices=SESSION_CHOICES,
        blank=True, null=True, default=''
    )


# year track_num order presenter title source_link

class Sponsor(models.Model):  # 후원사
    image_url = models.TextField('로고', null=True, default='')
    introduction = models.TextField('소개글', null=True, default='')
    homepage_link = models.TextField('홈페이지', default='')

    Platinum, Gold, Silver = 'Platinum', 'Gold', 'Silver'
    SPONSORSHIP_CHOICES = [
        (Platinum, 'Platinum'), (Gold, 'Gold'), (Silver, 'Silver'),
    ]
    sponsorship_rating = models.CharField('후원등급', max_length=50, choices=SPONSORSHIP_CHOICES,
                                          blank=True, null=True, default='')

    name = models.CharField('기업이름', max_length=50, null=True, default='')

# Sponsor : introduction, homepage_link, sponsorship_rating, name
