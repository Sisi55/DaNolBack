

> 파이참 IDE 사용중 - 가상환경 자동생성
>
> [패키치 설치 참고](https://velog.io/@lemontech119/DRF%EB%A1%9C-api-%EC%84%9C%EB%B2%84-%EA%B0%9C%EB%B0%9C0)
>
> [eb cli 설치 참고](https://docs.aws.amazon.com/ko_kr/elasticbeanstalk/latest/dg/eb-cli3-install-windows.html)

```python
# 패키지 설치
pip install django
pip install djangorestframework
pip install awsebcli --upgrade --user
pip install django-cors-headers

pip freeze > requirements.txt
```

> 저는 이렇게 했지만 여러분은
>
> ```python
> pip install -r requirements.txt
> ```
>
> 하시면 됩니다!



```python
# 장고 세팅 - 제가 해서 여러분은 안하셔도!
django-admin startproject config .
python manage.py startapp sheets
```



> config/settings.py 세팅을 했습니다



> [구글 스프레드시트 api](https://developers.google.com/sheets/api/quickstart/python)

```python
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
# 유튜브1 gspread
pip install gspread oauth2client
# 공식문서 ?
google-api-python-client
google-auth-httplib2
google-auth-oauthlib
```













