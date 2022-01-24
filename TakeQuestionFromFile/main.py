# with open('../token_immediate_sender.txt') as token_file:
#     TOKEN = token_file.read()
#
# token_file.close()

# with open('../site_code.html') as site_code_file:
#     string_file = site_code_file.read()
#     REQUIRED_CLASS = "student-session-question-title"
#     found_index = string_file.find(REQUIRED_CLASS)
#     last_index = 0
#     for i in range(len(string_file)):
#         if string_file[found_index + len(REQUIRED_CLASS) + 3 + i] == '<':
#             last_index = i + 1
#             break
#     site_code_file.close()
#
# question = string_file[(found_index + len(REQUIRED_CLASS) + 2):(found_index + len(REQUIRED_CLASS) + 2 + last_index)]
# print(question)

# -*- coding: utf-8 -*-
# encoding: utf-8
from __future__ import print_function

import os.path
import webbrowser
import pyperclip
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']


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

        previous_question = "Назвіть індустріальні об'єкти, які були побудовані у другій половині 50-х років - на " \
                            "початку 60-х років. "
        while True:
            with open('../site_code.html') as site_code_file:
                string_file = site_code_file.read()
                REQUIRED_CLASS = "student-session-question-title"
                found_index = string_file.find(REQUIRED_CLASS)
                last_index = 0
                for i in range(len(string_file)):
                    if string_file[found_index + len(REQUIRED_CLASS) + 3 + i] == '<':
                        last_index = i + 1
                        break
                site_code_file.close()

            question = string_file[(found_index + len(REQUIRED_CLASS) + 2):(found_index + len(REQUIRED_CLASS) + 2
                                                                            + last_index)]
            if question != previous_question:
                previous_question = question
                pyperclip.copy(question)
                time.sleep(2)
                query = "https://www.google.com/"
                print(query)
                webbrowser.open(query)
                print(question)
                with open('all_questions.txt', 'a') as all_question_file:
                    all_question_file.write(question + '\n')
                all_question_file.close()

                with open('previous_questions.txt', 'r') as previous_questions_file:
                    previous_file_id = previous_questions_file.read()
                    service.files().delete(fileId=previous_file_id).execute()

                previous_questions_file.close()
                file_metadata = {'name': 'all_questions.txt'}
                media = MediaFileUpload('all_questions.txt', mimetype='text/plain')
                file = service.files().create(body=file_metadata,
                                              media_body=media,
                                              fields='id').execute()
                print('File ID: %s' % file.get('id'))
                with open('previous_questions.txt', 'w') as previous_questions_file:
                    previous_questions_file.write(file.get('id'))

                previous_questions_file.close()
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()
