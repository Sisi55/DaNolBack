[toc]

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

  
  





> 한글은 영문으로 변경될 예정입니다 
>
> (현재 모델링된 내용을 바탕으로 작성한 것이니 변경되었으면 하는 부분은 알려주세요)
>
> 예시 response 가 잘 전달이 안된다면, 어떤 부분이 더 자세하면 좋을지 알려주세요
>
> - #### 준비위 api / 연사자 api
>
> ```python
> {
>     "길이": 32,
>     "구분": "준비위", # or 발표자
>     "data": [
>         {
>             "id": 1,
>             "구분": "준비위", # or 발표자
>             "이메일": "sisi.sisi.com",
>             "사진url": "...구글 드라이브로 공유할 생각이었습니다",
>             "이름": "김데놀",
>             "소개": "데이터야놀자 어쩌구저쩌구솰라"
>             "sns계정":[
>                 {
>                     "id": 1
>                     "구분": "깃허브",
>                 	"주소url": "github.com/xxxx"
>                 },                
>             ]
>         }, ...
>     ]
> }
> ```
>
> - #### 타임테이블 api (2020ver) 
>
>   - 발표자료 가져오기 api 와 동일한 response
>
> - #### 후원기업 api
>
> ```python
> {
>     "길이": 32,
>     "data": [
>         {
>             "id": 1,
>             "로고url": "...구글 드라이브로 공유할 생각이었습니다",
>             "소개": "데이터야놀자 어쩌구저쩌구솰라",
>             "기업이름": "주데놀",
>             "홈페이지url": "naver.com"
>         }, ...
>     ]
> }
> ```



