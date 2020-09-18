from __future__ import print_function
import pickle
import os.path

# from django.conf import settings
from django.db import transaction
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from config import settings
from openpyxl import load_workbook
from pyexcel_xlsx import get_data as xlsx_get

from sheets.models import Member, Content, Sponsor
from sheets.serializers import ContentSerializer, SponsorSerializer, MemberSerializer, ContentToPresenterSerializer


@api_view(['GET'])
def test_api(request):
    return Response({"message": "test ok."}, status=status.HTTP_200_OK)


@api_view(['GET'])
def test_y_api(request):
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets', \
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name( \
        os.path.join(settings.BASE_DIR, 'env/etc/creds.json'), scope)

    client = gspread.authorize(creds)

    # sheet = client.open("2020코딩테스트").get_worksheet(1)  # Open the spreadhseet # return class WorkSheet
    sheet = client.open("데이터야놀자2020 아카이빙 준비").get_worksheet(1)
    print(sheet.title)  # 첫번째 탭 제목 출력된다
    print(sheet.row_count, sheet.col_count)
    print(sheet.frozen_row_count)

    # for row in range(sheet.row_count):
    #     for col in range(sheet.col_count):
    #         sheet.cell(row,col) # return class Cell

    get_all_values = sheet.get_all_values()
    print(get_all_values)

    # print(sheet)
    # data = sheet.row_values(0)  # Get a list of all records
    return Response(get_all_values, status=status.HTTP_200_OK)


@api_view(['GET'])
def test_sheet_api(request):
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    # The ID and range of a sample spreadsheet.
    # TODO 시트ID 보안처리
    SAMPLE_SPREADSHEET_ID = '1alBaNJVw_rfCx5Wr7NTZfsBXvRoPAIeWapRRexLh7XU'

    """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # if os.path.exists('token.pickle'):
    #     with open('token.pickle', 'rb') as token:
    #         creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file( \
                os.path.join(settings.BASE_DIR, 'env/etc/credentials.json'), \
                # settings.BASE_DIR+'/env/etc/credentials.json',
                SCOPES,
                redirect_uri='http://localhost:8000/sheets/test/callback/')  # ,        'sheets/test/'
            print('flow:\n', flow)
            creds = flow.run_local_server(port=8000)
            print('creds:\n', creds)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                # range=SAMPLE_RANGE_NAME
                                ).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('RESULT:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[4]))

    return Response({"message": "test ok."}, status=status.HTTP_200_OK)


@api_view(['POST'])
@transaction.atomic
def save_archiving_data(request):  # 기존 엑셀 데이터를 db 에 저장하는 API
    if request.method == 'POST':

        api_key = request.query_params.get('apiKey')  # 아주 간단하게 인증 : post 니까!
        if api_key != settings.API_KEY:
            return Response({"message": "Request Permission Error."}, status=status.HTTP_403_FORBIDDEN)

        DATA_LEN = {
            '2016': 16,
            '2017': 33,
            '2018': 42,
            '2019': 23,
        }
        max_data_len = max(DATA_LEN.values())
        print('max_data_len', max_data_len)

        file = request.FILES['file']
        data = xlsx_get(file, row_limit=max_data_len)  # DATA_LEN[year]
        # print('data type', type(data)) # ordered dict
        # print('data', data[year][0][0])

        content_list = []
        for key_year, value_data_len in DATA_LEN.items():

            data[key_year] = data[key_year][1:]  # header 제외
            # content_list = []
            for row in data[key_year]:
                if row == []:
                    break
                print('row all', row)
                # print('year', row[0])
                # print('track_num', row[1])
                # print('order', row[2])
                # print('presenter_name', row[3])
                # print('title', row[4])
                if len(row) == 5:  # email
                    row.append("")
                    row.append("")
                if len(row) == 6:  # resource link
                    row.append("")

                # 발표자 생성 : TODO 사실 다시 덮어쓰려면 가져와서 수정하는 작업이 필요하다
                presenter = Member(name=row[3])
                # 발표 생성
                content = Content(year=row[0], track_num=row[1], order=row[2], presenter=presenter, title=row[4],
                                  source_link=row[6])
                presenter.save()
                content.save()
                content_list.append(ContentSerializer(instance=content).data)  # test

    return Response({
        # 'year': year,
        'size': len(content_list),  # DATA_LEN[year],
        'data': content_list,  # data[year],
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@transaction.atomic
def save_sponsor_data(request):
    data_len = request.query_params.get('size')  # 데이터 길이 수동 입력
    # 시트 이름은 어떻게 하지! 일단 하드코딩 : 'Form Responses 1'

    # 간단한 인증 : 홈페이지 데이터라서
    api_key = request.query_params.get('apiKey')  # 아주 간단하게 인증 : post 니까!
    if api_key != settings.API_KEY:
        return Response({"message": "Request Permission Error."}, status=status.HTTP_403_FORBIDDEN)

    # 파일 받아오기
    file = request.FILES['file']
    data = xlsx_get(file, row_limit=int(data_len))  # DATA_LEN[year]

    data['Form Responses 1'] = data['Form Responses 1'][1:]  # header 제외

    content_list = []
    for row in data['Form Responses 1']:
        # print('row all', row)
        # print('name', row[1])
        # print('homepage', row[6])
        # print('introduction', row[7])
        data = {
            'name': row[1],
            'homepage_link': row[6],
            'introduction': row[7],
            'sponsorship_rating': row[8],
        }

        # 이미 있는지 확인해봐야 하는데! 후원기업 이름 기반으로 확인하기
        existing_sponsor = Sponsor.objects.filter(name=row[1]).first()
        if existing_sponsor is not None:  # 이미 있으면
            sponsor_serializer = SponsorSerializer(existing_sponsor, data=data)
        else:
            sponsor_serializer = SponsorSerializer(data=data)

        if not sponsor_serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        # sponsor = Sponsor(introduction=row[7], homepage_link=row[6], sponsorship_rating=row[8], name=row[1])
        sponsor_serializer.save()

        # sponsor_serializer = SponsorSerializer(instance=sponsor)
        content_list.append(sponsor_serializer.data)

    return Response({
        'size': len(content_list),
        'data': content_list,
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def save_committee_data(request):
    data_len = request.query_params.get('size')  # 데이터 길이 수동 입력
    # 시트 이름은 어떻게 하지! 일단 하드코딩 : '설문지 응답 시트1'
    sheet_name = '설문지 응답 시트1'

    # 간단한 인증 : 홈페이지 데이터라서
    api_key = request.query_params.get('apiKey')  # 아주 간단하게 인증 : post 니까!
    if api_key != settings.API_KEY:
        return Response({"message": "Request Permission Error."}, status=status.HTTP_403_FORBIDDEN)

    # 파일 받아오기
    file = request.FILES['file']
    data = xlsx_get(file, row_limit=int(data_len))  # DATA_LEN[year]

    data[sheet_name] = data[sheet_name][1:]  # header 제외
    print(len(data[sheet_name]))

    content_list = []
    for row in data[sheet_name]:
        print('row all', row)
        if not row:  # 시트 행 != 실제 행 : 중간에 생략된 행 번호가 있네
            break
        # content_list.append(row)

        # Member: kind=PreparatoryCommittee email name introduction

        # print('name', row[1])
        # print('email', row[4])
        # print('introduction', row[3])

        data = {
            'name': row[1],
            'email': row[4],
            'introduction': row[3],
            'kind': Member.PreparatoryCommittee
        }
        # content_list.append(data)

        # # 이미 있는지 이름 기반으로 확인하기
        existing_committee = Member.objects.filter(name=row[1]).first()

        if existing_committee is not None:  # 이미 있으면
            member_serializer = MemberSerializer(existing_committee, data=data)
        else:
            member_serializer = MemberSerializer(data=data)

        if not member_serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        member_serializer.save()

        # content_list.append(member_serializer.validated_data)
        content_list.append(member_serializer.data)

    return Response({
        'size': len(content_list),
        'data': content_list,
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def save_content2020_data(request):
    data_len = request.query_params.get('size')  # 데이터 길이 수동 입력
    # 시트 이름 하드코딩
    sheet_name = '시트1'

    # 간단한 인증 : 홈페이지 데이터라서
    api_key = request.query_params.get('apiKey')  # 아주 간단하게 인증 : post 니까!
    if api_key != settings.API_KEY:
        return Response({"message": "Request Permission Error."}, status=status.HTTP_403_FORBIDDEN)

    # 파일 받아오기
    file = request.FILES['file']
    data = xlsx_get(file, row_limit=int(data_len))  # DATA_LEN[year]

    data[sheet_name] = data[sheet_name][1:]  # header 제외
    print(len(data[sheet_name]))

    content_list = []
    for row in data[sheet_name]:
        # print('row all', row)
        if not row:  # 시트 행 != 실제 행 : 중간에 생략된 행 번호가 있네
            print('row is []')
            break
        # content_list.append(row)

        # Member: email, name, belongTo
        # print('name', row[1])
        # print('email', row[9])
        # print('belongTo', row[2])
        presenter_data = {
            'name': row[1],
            'email': row[9],
            'belongTo': row[2],
        }
        # 이미 있는지 email 기반으로 확인하기
        existing_member = Member.objects.filter(email=row[9]).first()
        if existing_member is not None:  # 이미 있으면
            member_serializer = MemberSerializer(existing_member, data=presenter_data)
        else:
            member_serializer = MemberSerializer(data=presenter_data)
        if not member_serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        member_serializer.save()  ## TODO save

        # Content: presenter, title, presentation_time, introduction, kind
        # print('presenter', presenter_data)
        if not row[6]:
            row[6] = ' '
            print('title', row[6])
        if not row[7]:
            row[7] = ' '
            print('introduction', row[7])

        # print('presentation_time', row[5])
        # print('introduction', row[7])
        # print('kind', row[0])

        content_data = {
            'presenter': member_serializer.instance,  # for update
            'title': row[6],
            'presentation_time': row[5],
            'introduction': row[7],
            'kind': row[0],
        }
        # # content_list.append(data)

        # 발표자 email 기반으로 Content 찾아온다
        existing_content = Content.objects.filter(presenter__email=row[9]).first()
        if existing_content is not None:  # 이미 있으면
            content_serializer = ContentSerializer(existing_content, data=content_data)
        else:
            content_serializer = ContentSerializer(data=content_data)

        if not content_serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        content_serializer.save(presenter=member_serializer.instance)  ## TODO save

        # content_list.append(content_serializer.validated_data)
        content_list.append(content_serializer.data)

    return Response({
        'size': len(content_list),
        'data': content_list,
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_contents(request):
    year = request.query_params.get('year')
    print('year', year)

    content_list = Content.objects.filter(year=year)
    TRACK = {
        '2016': 3,
        '2017': 3,
        '2018': 4,
        '2019': 3,
    }

    track_data = {}
    for track in range(1, TRACK[year] + 1):
        content_track = content_list.filter(track_num=str(track))
        content_serializer = ContentSerializer(instance=content_track, many=True)
        track_data[f"track{track}"] = content_serializer.data

    return Response({
        'size': len(content_list),
        'year': year,
        'data': track_data,  # content_serializer.data,
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_sponsors(request):
    sponsor_list = Sponsor.objects.all()

    rating_data = {}
    ratings = [Sponsor.Platinum, Sponsor.Gold, Sponsor.Silver]
    for rating in ratings:
        sponsor_rating = sponsor_list.filter(sponsorship_rating=rating)
        sponsor_serializer = SponsorSerializer(instance=sponsor_rating, many=True)
        rating_data[rating] = sponsor_serializer.data

    return Response({
        'size': len(sponsor_list),
        # 'year': year,
        'data': rating_data,  # content_serializer.data,
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_members(request):
    member_list = Member.objects.filter(kind=Member.PreparatoryCommittee)
    member_serializer = MemberSerializer(instance=member_list, many=True)

    return Response({
        'size': len(member_serializer.data),
        'data': member_serializer.data,  # content_serializer.data,
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_contents_2020_TMP(request):
    content_list = Content.objects.filter(year='2020')
    content_serializer = ContentSerializer(instance=content_list, many=True)

    return Response({
        'size': len(content_serializer.data),
        'data': content_serializer.data,  # content_serializer.data,
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_presenters_2020_TMP(request): # 'presenter__sns',
    content_list = Content.objects.filter(year='2020')#.values('presenter__id', 'presenter__kind', 'presenter__email', 'presenter__name', 'presenter__introduction',  'presenter__belongTo')
    presenter_list = []
    for content in content_list:
        presenter_list.append(content.presenter)
    print(type(content_list))
    presenter_serializer = ContentToPresenterSerializer(instance=presenter_list, many=True)
    # if not content_serializer.is_valid(raise_exception=True):
    #     return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

    return Response({
        'size': len(presenter_serializer.data),
        'data': presenter_serializer.data,  # content_serializer.data,
    }, status=status.HTTP_200_OK)
