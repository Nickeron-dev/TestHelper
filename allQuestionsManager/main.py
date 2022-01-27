from __future__ import print_function

import codecs
import os.path
import requests
import io

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

with open('../token_main.txt') as token_file:
    TOKEN = token_file.read()

token_file.close()

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
bot_chatID = -668820576
content_previous = ''


def main():
    global content_previous
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v2', credentials=creds)
        repeated_questions = {}
        while True:
            file_id_illia = '1sqjrxQE7PruFH0qp7j8tzWUH6arJylkg'
            text_illia = service.files().get_media(fileId=file_id_illia).execute().decode('utf-8').encode('Windows-1251').decode('Windows-1251')  # with .decode('utf-8') also works
            file_id_daria = '1if3GwNgPMyod72awNrHyHrMi3mZxfij2'
            text_daria = service.files().get_media(fileId=file_id_daria).execute().decode('Windows-1251')
            file_id_artem = '1lRcbZqKv1vWL-xK7vxayEha7pdjl6A2t'
            text_artem = service.files().get_media(fileId=file_id_artem).execute().decode('utf-8')
            content_new = 'ILLIA:\n\n' + text_illia + '\n\nDARIIA:\n\n' + text_daria + '\n\nARTEM:\n\n' + text_artem

            if content_new != content_previous:
                print(content_new)
                send_text_1 = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + bot_chatID.__str__() \
                              + '&parse_mode=Markdown&text=' + 'Updated: '
                send_text_2 = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + bot_chatID.__str__() \
                              + '&parse_mode=Markdown&text=' + content_new
                requests.get(send_text_1)
                requests.get(send_text_2)
                content_previous = content_new

            line_i = ''
            line_j = ''
            for i in range(len(content_new)):
                print(line_i)
                if content_new[i] != '\n':
                    line_i += content_new[i]
                    continue
                else:
                    count = 0
                    for j in range(i + 1, len(content_new)):
                        if content_new[j] != '\n':
                            line_j += content_new[j]

                        else:
                            if line_i == line_j and line_i != '' and (
                                    not repeated_questions.keys().__contains__(line_i) or repeated_questions.get(
                                    line_i) < 2):
                                count += 1
                                if not repeated_questions.keys().__contains__(line_i):
                                    print('here')
                                    repeated_questions[line_i] = 1
                                    repeat_warning = 'WARNING!!!\nQuestion: ' + line_i + '\nHas been repeated!!!'
                                    send_warning = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' \
                                                   + bot_chatID.__str__() + '&parse_mode=Markdown&text=' + repeat_warning
                                    requests.get(send_warning)
                                else:
                                    if count > 1:
                                        print('send')
                                        repeated_questions[line_i] += 1
                                        repeat_warning = 'WARNING!!!\nQuestion: ' + line_i + '\nHas been repeated!!!'
                                        send_warning = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' \
                                                       + bot_chatID.__str__() + '&parse_mode=Markdown&text=' + repeat_warning
                                        requests.get(send_warning)

                            line_j = ''

                    line_i = ''
    except HttpError as error:
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()
