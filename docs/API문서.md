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
  > data : 해당 연도 '발표' 배열
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
  
- > 범위 외 연도 입력하면
  >
  > ```python
  > {
  >     "size": 0,
  >     "data": []
  > }
  > ```



---









