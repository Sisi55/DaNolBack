[toc]

##### 목차

> Ctrl + F 로 찾아주세요!

- 발표자료 가져오기
- 후원기업 api
- 준비위 api
- 임시) 2020 발표 list 가져오기
- 임시) 2020 발표자 list 가져오기



> ##### BASE_URL
>
> - http://danol-env.ap-northeast-2.elasticbeanstalk.com



## 발표자료 가져오기

- ##### URL

  - GET
  - BASE_URL + /sheets/contents/?year={연도}
  - 연도 : 2016~2020

- ##### response

  - > size : 해당 연도 data 길이
    >
    > year : 연도
    >
    > data : 해당 연도 track 별 '발표' 배열
    >
    > ```python
    > # response 일부
    > "data":{
    >     "track1": [발표배열],
    >     "track2": [발표배열],
    >     # 2018은 track 이 4개 있으니 유의해주세요 (나머지는 3 track)
    > }
    > ```
    >
    > 
  
    > | 속성이름    | 속성설명                                                     |
    > | ----------- | ------------------------------------------------------------ |
    > | id          | 발표 id                                                      |
    > | year        | 발표 연도                                                    |
    > | track_num   | 트랙번호                                                     |
    > | order       | 발표 순서                                                    |
    > | presenter   | 발표자 정보 <br /> { id : 발표자 id<br /> kind : member 구분 (발표자/준비위)<br /> email : 이메일<br /> image_url : 사진url<br /> name : 이름<br /> introduction : 소개글<br /> sns : 계정정보 } |
    > | title       | 발표 제목                                                    |
    > | source_link | 자료 링크                                                    |
    >
    > 추가로 2020 연도의 데이터에는
    >
    > | 속성이름          | 속성설명 |
    > | ----------------- | -------- |
    > | presentation_time | 발표시간 |
    > | difficulty        | 난이도   |
    >
    > 가 추가될 예정입니다!
  
  - ```python
    {
        "size": 32,
        "year": "2017",
        "data": {
            "track1": [
                {
                    "id": 16,
                    "year": "2017",
                    "track_num": "1",
                    "order": "1",
                    "presenter": {
                        "id": 16,
                        "kind": "발표자",
                        "email": null,
                        "image_url": null,
                        "name": "김상우",
                        "introduction": null,
                        "sns": []
                    },
                    "title": "비트윈 데이터분석팀의 하루",
                    "source_link": "https://speakerdeck.com/swkimme/biteuwin-deiteotimyi-haru"
                },
                {...}
            ],
            "track2": [
                {
                    "id": 27,
                    "year": "2017",
                    "track_num": "2",
                    "order": "12",
                    "presenter": {
                        "id": 27,
                        "kind": "발표자",
                        "email": null,
                        "image_url": null,
                        "name": "이주형",
                        "introduction": null,
                        "sns": []
                    },
                    "title": "데이터 과학자가 일 잘 하는 법에 대한 흔하지 않은 이야기",
                    "source_link": "https://drive.google.com/file/d/0B7URaKiuWhUaVTBNY0VhNWhXalk/view"
                },
                {...},
            ],
            "track3": [
                {
                    "id": 38,
                    "year": "2017",
                    "track_num": "3",
                    "order": "23",
                    "presenter": {
                        "id": 38,
                        "kind": "발표자",
                        "email": null,
                        "image_url": null,
                        "name": "성동찬",
                        "introduction": null,
                        "sns": []
                    },
                    "title": "데이터야 안전하게 놀아보자",
                    "source_link": "https://drive.google.com/file/d/0B1PDX9LaTv_xYVFUbVp2Ti1waUU/view"
                },
            ]
        }
    }
    ```






## 후원기업 api

- url : GET

  - BASE_URL + /sheets/sponsors/
- response

| 속성이름           | 속성설명                                                    |
| ------------------ | ----------------------------------------------------------- |
| size               | 전체 데이터 길이                                            |
| data               | 등급별 후원기업 나열하였습니다<br /> (Platinum/Gold/Silver) |
| introduction       | 후원 기업 소개글                                            |
| homepage_link      | 홈페이지 링크                                               |
| sponsorship_rating | 후원 등급                                                   |
| name               | 후원 기업 이름                                              |



```python
{
    "size": 6,
    "data": {
        "Platinum": [
            {
                "id": 1,
                "introduction": "네이버는 대한민국 No1 기술플랫폼 기업이며 쇼핑, 금융, 광고, 동영상, UGC 등 다양한 서비스를 제공합니다. 특히 라인을 비롯하여 스노우, 웹툰, Vlive의 성공을 통해 글로벌 서비스의 한류를 리딩하고 있습니다. 최근 수년간 매출의 1/4을 R&D 투자중이며 특히 클로바, 네이버랩스, 그리고 네이버랩스유럽을 통해 AI와 로보틱스 분야에서 글로벌 수준의 경쟁력을 보여주고 있습니다. 더나아가 최근 한국,일본, 동남아, 유럽을 잇는 Global AI R&D Belt 구축을 통해 진정한 글로벌 기술기업으로 거듭나고 있습니다.",
                "homepage_link": "https://www.navercorp.com/",
                "sponsorship_rating": "Platinum",
                "name": "네이버"
            },
            {
                "id": 3,
                "introduction": "국내 1위 배달앱 배달의민족을 운영하는 ‘우아한형제들’은 '좋은 음식을 먹고 싶은 곳에서'라는 비전 아래, 배달이 안 되던 외식업소의 음식을 배달해주는 '배민라이더스',  음식업종 자영업자에게 좋은 품질의 배달용품을 합리적인 가격에 제공하는 '배민상회' 등으로 배달문화를 바꿔 나가고 있습니다. \n  또한 종합 '푸드테크' 기업으로 나아가기 위하여 해외시장 진출 등의 글로벌 사업과 자율주행 로봇 기술 개발 등의 미래사업으로 사업확장을 준비, 진행하고 있습니다.",
                "homepage_link": "https://www.woowahan.com/",
                "sponsorship_rating": "Platinum",
                "name": "우아한형제들"
            },
            {
                "id": 4,
                "introduction": "2012년 설립된 Elastic 은 오픈 소스를 기반으로 설립된 검색 기업입니다. Elastic 은 어디에서나 배포될 수 있는 기술 스택인 Elastic Stack 을 기반으로, 엔터프라이즈 검색, 통합 가시성, 보안을 위한 솔루션 들을 제공합니다. 전 세계 수천 개의 기업들이 Elastic 을 이용해 업무상 중요한 시스템을 구동하고 문제를 해결하고 있습니다.",
                "homepage_link": "https://www.elastic.co",
                "sponsorship_rating": "Platinum",
                "name": "Elastic"
            }
        ],
        "Gold": [
            {
                "id": 2,
                "introduction": "추후 제출 요청",
                "homepage_link": "https://learningspoons.com/",
                "sponsorship_rating": "Gold",
                "name": "러닝스푼즈"
            },
            {
                "id": 5,
                "introduction": "추후 발송 예정",
                "homepage_link": "http://www.ebrain.kr/",
                "sponsorship_rating": "Gold",
                "name": "주식회사 이브레인"
            }
        ],
        "Silver": [
            {
                "id": 6,
                "introduction": "한빛미디어는 ‘책으로 여는 IT 세상’을 만들어 갑니다. IT 세상의 주역은 ‘우리’ 입니다. 한빛미디어는 IT 세상의 주역들을 위한 프로그래밍, 컴퓨터공학, IT 에세이, Make, OA, 그래픽, 나와 내 아이를 위한 실용 등 다양한 분야의 책으로 IT 세상을 만들어 가고 있습니다.",
                "homepage_link": "https://www.hanbit.co.kr/",
                "sponsorship_rating": "Silver",
                "name": "한빛미디어"
            }
        ]
    }
}
```





## 준비위 api

- url : GET
  - BASE_URL + /sheets/committee-members/
- response

| 속성이름     | 속성설명                                                     |
| ------------ | ------------------------------------------------------------ |
| size         | 데이터 길이                                                  |
| data         | 실제 데이터                                                  |
| email        | 준비위 이메일                                                |
| name         | 준비위 이름                                                  |
| introduction | 준비위 한줄 소개                                             |
| sns          | (*소셜 계정 정보를 넣으려고 모델링한 곳인데 프론트에서 이 정보를 어떻게 출력하실지 몰라 데이터를 채우지 않았습니다*) |

```python
{
    "size": 19,
    "data": [
        {
            "id": 149,
            "kind": "준비위",
            "email": "dnlriver@naver.com",
            "image_url": null,
            "name": "공태웅",
            "introduction": "컨텐츠 파트 팀원",
            "sns": []
        },
        {
            "id": 150,
            "kind": "준비위",
            "email": "soryeongk.kr@gmail.com",
            "image_url": null,
            "name": "김소령",
            "introduction": "홈페이지 파트 팀원",
            "sns": []
        },
        {
            "id": 151,
            "kind": "준비위",
            "email": "dqgsh1055@gmail.com",
            "image_url": null,
            "name": "김시현",
            "introduction": "컨텐츠 / 홈페이지 / 뉴스레터 파트 팀원",
            "sns": []
        },
    ]
}
```





## 임시) 2020 발표 list 가져오기

- url : GET
  - BASE_URL + /sheets/contents-2020/

```python
{
    "size": 24,
    "data": [
        {
            "id": 427,
            "year": "2020",
            "track_num": "",
            "order": "",
            "presenter": {
                "id": 425,
                "kind": "발표자",
                "email": "pbj00812@gmail.com",
                "image_url": "",
                "name": "박범진",
                "introduction": "",
                "sns": [],
                "belongTo": "wadiz"
            },
            "title": "데이터로 이야기하는 재미",
            "source_link": "",
            "introduction": "회사 내에서 이야기를 통해 일하는 방법",
            "kind": "일반 세션"
        },
        {
            "id": 428,
            "year": "2020",
            "track_num": "",
            "order": "",
            "presenter": {
                "id": 426,
                "kind": "발표자",
                "email": "ym911.jo@sk.com",
                "image_url": "",
                "name": "Jerry(조영민)",
                "introduction": "",
                "sns": [],
                "belongTo": "FLO (드림어스컴퍼니)"
            },
            "title": "빌런들 속에서 데이터팀 만들기(부제 :  Data Literacy 역량을 갖춘 조직 만들기)",
            "source_link": "",
            "introduction": "500만 가입자를 가진 음악서비스 플랫폼 FLO에서 뮤직데이터팀 빌딩 과정을 공유 하고자 합니다.",
            "kind": "일반 세션"
        },
        {
            "id": 429,
            "year": "2020",
            "track_num": "",
            "order": "",
            "presenter": {
                "id": 427,
                "kind": "발표자",
                "email": "kbkb456@gmail.com",
                "image_url": "",
                "name": "임광빈",
                "introduction": "",
                "sns": [],
                "belongTo": "크로키닷컴 (UX팀)"
            },
            "title": "UX 필살기 커맨드 AB",
            "source_link": "",
            "introduction": "지그재그 앱 내에서 했던 AB테스트 사례",
            "kind": "일반 세션"
        },
    ]
}
```



## 임시) 2020 발표자 list 가져오기

- url : GET
  - BASE_URL + /sheets/presenters-2020/

```python
{
    "size": 24,
    "data": [
        {
            "id": 425,
            "kind": "발표자",
            "email": "pbj00812@gmail.com",
            "name": "박범진",
            "introduction": "",
            "belongTo": "wadiz"
        },
        {
            "id": 426,
            "kind": "발표자",
            "email": "ym911.jo@sk.com",
            "name": "Jerry(조영민)",
            "introduction": "",
            "belongTo": "FLO (드림어스컴퍼니)"
        },
    ]
}
```

