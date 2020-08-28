from __future__ import print_function
import pickle
import os.path
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
def test_excel_api(request):
    # print('api send')
    if request.method == 'POST':
        # print('api post')
        file = request.FILES['file']
        data = xlsx_get(file, row_limit=50)

        sheet = data["2016"] # sheet
        for s in sheet:
            print(s)

        # data_only=Ture로 해줘야 수식이 아닌 값으로 받아온다.
        # load_wb = load_workbook(file, data_only=True)
        #
        # # 시트 이름으로 불러오기
        # load_ws = load_wb['2016']
        # print(load_ws.title)
        #
        # # 일단 리스트에 담기
        # all_values = []
        # for row in load_ws.rows:
        #     row_value = []
        #     for cell in row:
        #         print(cell.value, type(cell.value))
        #         row_value.append(cell.value)
        #     all_values.append(row_value)
        # print(all_values)

    return Response({"message": data}, status=status.HTTP_200_OK)
