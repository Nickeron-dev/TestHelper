from __future__ import print_function

import io
import os.path
import requests

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# If modifying these scopes, delete the file token.json.
from googleapiclient.http import MediaIoBaseDownload

with open('../token_main.txt') as token_file:
    TOKEN = token_file.read()

token_file.close()

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
bot_chatID = -668820576


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))

        while True:
            try:
                with open('../previous_questions.txt', 'r') as previous_questions_file:
                    previous_file_id = previous_questions_file.read()

                previous_questions_file.close()

                with open('questions_illia.txt', 'r') as previous:
                    content_previous = previous.read()

                previous.close()
                request = service.files().get_media(fileId=previous_file_id)
                fh = io.BytesIO()
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    print("Download %d%%." % int(status.progress() * 100))
            except HttpError as exc:
                print("OK")
                continue

            with io.open("new_questions_illia.txt", "wb") as illias_questions:
                fh.seek(0)
                illias_questions.write(fh.read())

            with open('new_questions_illia.txt', 'r') as new_file:
                content_new = new_file.read()

            new_file.close()

            if content_new != content_previous:
                with open('questions_illia.txt', 'w') as current:
                    current.write(content_new)

                current.close()
                send_text_1 = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + bot_chatID.__str__() + '&parse_mode=Markdown&text=' + 'Updated:'
                send_text_2 = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + bot_chatID.__str__() + '&parse_mode=Markdown&text=' + content_new
                requests.get(send_text_1)
                requests.get(send_text_2)
                content_previous = content_new

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()
