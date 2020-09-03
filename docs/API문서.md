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

- ```python
  {
      "size": 15,
      "data": [
          {
              "id": 1,
              "year": "2016",
              "track_num": "1",
              "order": "1",
              "presenter": {
                  "id": 1,
                  "kind": "발표자",
                  "email": null,
                  "image_url": null,
                  "name": "김상우",
                  "introduction": null,
                  "sns": []
              },
              "title": "데이터 분석에서 가치 만들어내기",
              "source_link": "https://datayanolja.github.io/2017-datayanolja/slide/2016/1-%ED%82%A4%EB%85%B8%ED%8A%B8/%ED%82%A4%EB%85%B8%ED%8A%B8-1-%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EB%B6%84%EC%84%9D%EC%97%90%EC%84%9C%20%EA%B0%80%EC%B9%98%20%EB%A7%8C%EB%93%A4%EC%96%B4%EB%82%B4%EA%B8%B0-%EA%B9%80%EC%83%81%EC%9A%B0.pdf"
          },
          ...
      ]
  }
  ```
  
- 범위 외 연도 입력하면
  
  ```python
  {
   "size": 0,
   "data": []
  }
  ```



---









