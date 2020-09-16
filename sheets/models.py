from django.db import models


class Member(models.Model):  # 발표자/준비위

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

    email = models.CharField('이메일', max_length=30, null=True)
    image_url = models.TextField('사진', null=True)
    name = models.CharField('이름', max_length=15)
    introduction = models.TextField('소개글', null=True)


# Member: kind=PreparatoryCommittee email name introduction

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
        blank=True, null=True
    )
    link = models.TextField('sns링크')


# kind link

class Content(models.Model):  # 발표
    year = models.CharField('연도', max_length=5)
    track_num = models.CharField('트랙번호', max_length=2)
    order = models.CharField('발표순번', max_length=2)
    presenter = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="contents", null=True)
    title = models.TextField('발표제목')
    source_link = models.TextField('자료링크')

    presentation_time = models.CharField('발표시간', max_length=10, null=True)  # ver 2020
    difficulty = models.CharField('발표 난이도', max_length=15, null=True)  # ver 2020


# year track_num order presenter title source_link

class Sponsor(models.Model):  # 후원사
    image_url = models.TextField('로고', null=True)
    introduction = models.TextField('소개글', null=True)
    homepage_link = models.TextField('홈페이지')

    Platinum, Gold, Silver = 'Platinum', 'Gold', 'Silver'
    SPONSORSHIP_CHOICES = [
        (Platinum, 'Platinum'), (Gold, 'Gold'), (Silver, 'Silver'),
    ]
    sponsorship_rating = models.CharField('후원등급', max_length=50, choices=SPONSORSHIP_CHOICES,
                                          blank=True, null=True)

    name = models.CharField('기업이름', max_length=50, null=True)

# Sponsor : introduction, homepage_link, sponsorship_rating, name
