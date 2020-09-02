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

from sheets.models import Member, Content
from sheets.serializers import ContentSerializer


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
                if len(row) == 5: # email
                    row.append("")
                    row.append("")
                if len(row) == 6: # resource link
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


@api_view(['GET'])
def get_contents(request):
    year = request.query_params.get('year')
    print('year', year)

    content_list = Content.objects.filter(year=year)
    content_serializer = ContentSerializer(instance=content_list,many=True)

    return Response({
        'size':len(content_serializer.data),
        'data':content_serializer.data,
    }, status=status.HTTP_200_OK)